#!/usr/local/bin/python
# coding: utf8

from emoticon_algorithm import emoticonAlgorithm
import sentiment_analysis
from autolabel import autolabel
from senticnet import SenticScore
import numpy as np
import matplotlib.pyplot as plt

class TweetAnalysationResult:
	def __init__(self, emoticonResult, sasaResult, senticNetResult, nltkResult, sentiWordNetResult):
		self.emoticonResult = emoticonResult
		self.sasaResult = sasaResult
		self.senticNetResult = senticNetResult
		self.nltkResult = nltkResult
		self.sentiWordNetResult = sentiWordNetResult

class SentimentTotal:
	def __init__(self, positiveTotal, negativeTotal, neutralTotal, naTotal):
		self.positiveTotal = positiveTotal
		self.negativeTotal = negativeTotal
		self.neutralTotal = neutralTotal
		self.naTotal = naTotal
	def count(self, string):
		if(string == "positive" or string == "pos"):
			self.positiveTotal = self.positiveTotal + 1
		elif(string == "negative" or string == "neg"):
			self.negativeTotal = self.negativeTotal + 1
		elif(string == "neutral"):
			self.neutralTotal = self.neutralTotal + 1
		elif(string == "n/a" or string == "unsure"):
			self.naTotal = self.naTotal + 1
	def plot(self, filename):
		xaxis = range(4)
		bars = [self.positiveTotal, self.negativeTotal, self.neutralTotal, self.naTotal]
		labels = ["positive", "negative", "neutral", "unsure"]

		minY = 0
		maxY = 0
		
		for y in bars:
			if y > maxY:
				maxY = y
			if y < minY:
				minY = y

		fig = plt.figure(figsize=(8, 6))
		plt.subplots_adjust(bottom=0.15, left=0.10, right=0.90, top=0.95)

		plt.ylim([minY,maxY])
		plt.xticks(xaxis, labels, rotation='vertical', size='small', ha='center')
		rects = plt.bar(xaxis, bars, 0.5, alpha=0.4, color='b', align="center")
		autolabel(rects)
		rects[0].set_color('g')
		rects[1].set_color('r')
		rects[2].set_color('y')
		rects[3].set_color('0.5')
		plt.savefig(filename)
		plt.clf()
		plt.close()

	def __str__(self):
		return "positive: " + str(self.positiveTotal) + ", negative: " + str(self.negativeTotal) + ", neutral: " + str(self.neutralTotal) + ", unsure: " + str(self.naTotal)

def analyseTweet(tweet, sasaInstance, senticNetInstance, sentiWordNetInstance, nltkTweetClassifierInstance):
	emoticonRes = emoticonAlgorithm(tweet) #returns a string "neurtal", "negative", "positive", "n/a"
	sasaRes = sasaInstance.classifyTweet(tweet)
	sasaResReformated = [sasaRes[0], sasaRes[1]] #[0] = unicode "neutral", "negative", "positive", "unsure" [1] = score (float; negative values = negative, positive values = positive)
	senticNetRes = senticNetInstance.getTweetSenticScore(tweet) #SenticScore object

	nltkRes = nltkTweetClassifierInstance.classifyTweet(tweet) #String "pos", "neg"

	sentiWordNetRes = sentiWordNetInstance.getTweetScore(tweet)  #float indicating wheter the tweet is positive (positive number) or negative (negative number)
	return TweetAnalysationResult(emoticonRes, sasaResReformated, senticNetRes, nltkRes, sentiWordNetRes)


def combineResults(resultList, titleFilePrefix, log):
	noTweets = len(resultList)

	emoticonTotal = SentimentTotal(0, 0, 0, 0)

	sasaTotal = SentimentTotal(0, 0, 0, 0)
	sasaAverage = 0.0

	senticnetTotal = SentimentTotal(0, 0, 0, 0)
	senticnetAverage = SenticScore(0, 0, 0, 0, 0)
	senticCount = 0

	nltkTotal = SentimentTotal(0, 0, 0, 0)

	sentiWordNetTotal = SentimentTotal(0, 0, 0, 0)
	sentiWordNetAverage = 0.0
	sentiWordNetCount = 0

	for r in resultList:
		#emoticon: just count
		emoticonTotal.count(r.emoticonResult)

		#sasa: count and calculate average
		sasaTotal.count(r.sasaResult[0])
		sasaAverage = sasaAverage + r.sasaResult[1]

		#senticnet: count and calculate average
		if(r.senticNetResult == None):
			senticnetTotal.count("unsure")
		elif(r.senticNetResult.calcTweetPolarity() > 0.001):
			senticnetTotal.count("positive")
		elif(r.senticNetResult.calcTweetPolarity() < -0.001):
			senticnetTotal.count("negative")
		else:
			senticnetTotal.count("neutral")

		if(r.senticNetResult != None):
			senticnetAverage.add(r.senticNetResult.average())
			senticCount = senticCount + 1

		#nltk: count
		nltkTotal.count(r.nltkResult)

		#sentiwordnet: count and calculate average
		if(r.sentiWordNetResult == None):
			sentiWordNetTotal.count("unsure")
		elif(r.sentiWordNetResult > 0.001):
			sentiWordNetTotal.count("positive")
		elif(r.sentiWordNetResult < -0.001):
			sentiWordNetTotal.count("negative")
		else:
			sentiWordNetTotal.count("neutral")

		if r.sentiWordNetResult != None:
			sentiWordNetAverage = sentiWordNetAverage + r.sentiWordNetResult
			sentiWordNetCount = sentiWordNetCount + 1

	#calculate averages
	sasaAverage = sasaAverage / noTweets

	senticnetAverage = SenticScore(
		senticnetAverage.pleasantness / senticCount,
		senticnetAverage.attention / senticCount,
		senticnetAverage.sensitivity / senticCount,
		senticnetAverage.aptitude / senticCount,
		senticnetAverage.polarity / senticCount
	)

	sentiWordNetAverage = sentiWordNetAverage / sentiWordNetCount

	log.log("emoticonTotal: " + str(emoticonTotal))

	log.log("sasaTotal: " + str(sasaTotal))
	log.log("sasaAvg: " + str(sasaAverage))

	log.log("senticnetTotal: " + str(senticnetTotal))
	log.log("senticnetAverage: " + str(senticnetAverage))

	log.log("nltkTotal: " + str(nltkTotal))

	log.log("sentiWordNetTotal: " + str(sentiWordNetTotal))
	log.log("sentiWordNetAverage: " + str(sentiWordNetAverage))

	emoticonTotal.plot("plots/" + titleFilePrefix+"_emoticon.svg")
	sasaTotal.plot("plots/" + titleFilePrefix+"_sasa.svg")
	nltkTotal.plot("plots/" + titleFilePrefix+"_nltk.svg")
	sentiWordNetTotal.plot("plots/" + titleFilePrefix+"_sentiwordnet.svg")
	sentiWordNetTotal.plot("plots/" + titleFilePrefix+"_sentiwordnet.svg")
	senticnetTotal.plot("plots/" + titleFilePrefix+"_senticnet_total.svg")
	senticnetAverage.plot("plots/" + titleFilePrefix+"_senticnet_avg.svg")