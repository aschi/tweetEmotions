#!/usr/local/bin/python
# coding: utf8

from emoticonAlgorithm import emoticonAlgorithm
import sentimentanalysis
from senticnet import SenticScore

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
	def __str__(self):
		return "positive: " + str(self.positiveTotal) + ", negative: " + str(self.negativeTotal) + ", neutral: " + str(self.neutralTotal) + ", unsure: " + str(self.naTotal)

class SentimentScore:
	def __init__(self, neg, pos, neutral):
		self.neg = neg
		self.pos = pos
		self.neutral = neutral

	def add(other):
		self.neg = self.neg + other.neg
		self.pos = self.post + other.pos
		self.neutral = self.neutral + other.neutral
	def __str__(self):
		return "neg: " + str(self.neg) + ", pos: " + str(self.pos) + ", neutral: " + str(self.neutral)

def analyseTweet(tweet, sasaInstance, senticNetInstance, sentiWordNetInstance, nltkTweetClassifierInstance):
	emoticonRes = emoticonAlgorithm(tweet) #returns a string "neurtal", "negative", "positive", "n/a"
	sasaRes = sasaInstance.classifyTweet(tweet)
	sasaResReformated = [sasaRes[0], sasaRes[1]] #[0] = unicode "neutral", "negative", "positive", "unsure" [1] = score (float; negative values = negative, positive values = positive)
	senticNetRes = senticNetInstance.getTweetSenticScore(tweet) #SenticScore object
	
	#sentiment API has limitations and is therefore no longer used
	#sentimentRes = sentimentanalysis.analyzeTweet(tweet) #Object [label=>("neg", "pos", "neutral"); probability=>[neg:float, neutral:float, pos:float]]
	
	nltkRes = nltkTweetClassifierInstance.classifyTweet(tweet) #String "pos", "neg"

	sentiWordNetRes = sentiWordNetInstance.getTweetScore(tweet)  #float indicating wheter the tweet is positive (positive number) or negative (negative number)
	return TweetAnalysationResult(emoticonRes, sasaResReformated, senticNetRes, nltkRes, sentiWordNetRes)


def combineResults(resultList):
	noTweets = len(resultList)

	emoticonTotal = SentimentTotal(0, 0, 0, 0)

	sasaTotal = SentimentTotal(0, 0, 0, 0)
	sasaAverage = 0.0

	senticnetAverage = SenticScore(0, 0, 0, 0, 0)
	senticCount = 0

	#sentimentTotal = SentimentTotal(0, 0, 0, 0)
	#sentimentAverage = SentimentScore(0, 0, 0)

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

		#senticnet: calculate average
		if(r.senticNetResult != None):
			senticnetAverage.add(r.senticNetResult)
			senticCount = senticCount + 1

		#sentiment: count and calculate average
		#sentimentTotal.count(r.sentimentRes["label"])
		#sentimentAverage.add(r.sentimentRes["probability"])

		#nltk: count
		nltkTotal.count(r.nltkResult)

		#sentiwordnet: count and calculate average
		if(r.sentiWordNetResult == None):
			sentiWordNetTotal.count("unsure")
		elif(r.sentiWordNetResult > 0):
			sentiWordNetTotal.count("positive")
		elif(r.sentiWordNetResult == 0):
			sentiWordNetTotal.count("neutral")
		else:
			sentiWordNetTotal.count("negative")

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

	#sentimentAverage = SentimentScore(
	#	sentimentAverage.neg / noTweets,
	#	sentimentAverage.pos / noTweets,
	#	sentimentAverage.neutral / noTweets,
	#)

	sentiWordNetAverage = sentiWordNetAverage / sentiWordNetCount

	print "emoticonTotal: " + str(emoticonTotal)

	print "sasaTotal: " + str(sasaTotal)
	print "sasaAvg: " + str(sasaAverage)

	print "senticnetAverage: " + str(senticnetAverage)

	#print "sentimentTotal: " + str(sentimentTotal)
	#print "sentimentAverage: " + str(sentimentAverage)

	print "nltkTotal: " + str(nltkTotal)

	print "sentiWordNetTotal: " + str(sentiWordNetTotal)
	print "sentiWordNetAverage: " + str(sentiWordNetAverage)