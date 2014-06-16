#!/usr/local/bin/python
# coding: utf8

import xml.etree.ElementTree as ET
import re
import numpy as np
import matplotlib.pyplot as plt
from preprocessing import preprocessTweet, getWordCombinations
from autolabel import autolabel

class SenticScore:
	def __init__(self, pleasantness, attention, sensitivity, aptitude, polarity):
		self.pleasantness = pleasantness
		self.attention = attention
		self.sensitivity = sensitivity
		self.aptitude = aptitude
		self.polarity = polarity
		self.count = 1
	def add(self, senticScore):
		self.count = self.count + 1
		self.pleasantness = self.pleasantness + senticScore.pleasantness
		self.attention = self.attention + senticScore.attention
		self.sensitivity = self.sensitivity + senticScore.sensitivity
		self.aptitude = self.aptitude + senticScore.aptitude
		self.polarity = self.polarity + senticScore.polarity
	def average(self):
		return SenticScore(self.pleasantness / self.count,
			self.attention / self.count,
			self.sensitivity / self.count,
			self.aptitude / self.count,
			self.polarity / self.count
		)

	def calcTweetPolarity(self):
		return (self.pleasantness+abs(self.attention)-abs(self.sensitivity)+self.aptitude)/(3*self.count)

	def __str__(self):
		return "pleasantness: " + str(self.pleasantness) + ", attention:" + str(self.attention) + ", sensitivity:" + str(self.sensitivity) + ", aptitude: " + str(self.aptitude)+ ", polarity: " + str(self.polarity)
	def plot(self, filename):
		xaxis = range(5)
		self.pleasantness, self.attention, self.sensitivity, self.aptitude, self.polarity
		bars = [self.pleasantness, self.attention, self.sensitivity, self.aptitude, self.polarity]
		labels = ["pleasantness", "attention", "sensitivity", "aptitude", "polarity"]

		minY = 0
		maxY = 0
		
		for y in bars:
			if y > maxY:
				maxY = y
			if y < minY:
				minY = y
		
		fig = plt.figure(figsize=(8, 6))
		plt.subplots_adjust(bottom=0.18, left=0.05, right=0.95, top=0.95)

		plt.ylim([minY,maxY])
		plt.xticks(xaxis, labels, rotation='vertical', size='small', ha='center')
		plt.axhline(0, color='black')
		rects = plt.bar(xaxis, bars, 0.5, alpha=0.4, color='b', align="center")
		autolabel(rects)
		rects[0].set_color('b')
		rects[1].set_color('r')
		rects[2].set_color('m')
		rects[3].set_color('g')
		rects[4].set_color('y')
		plt.savefig(filename)
		plt.clf()
		plt.close()

class SenticNet:
	def getTweetSenticScore(self, tweet):
		words = preprocessTweet(tweet)
		wordcombos = getWordCombinations(words, " ")
		total = SenticScore(0.0, 0.0, 0.0, 0.0, 0.0)
		count = 0

		for w in wordcombos:
			obj = self.getWordSenticScore(w)
			if obj != None:
				total.add(obj)
				count = count + 1
		
		if count > 0:
			return total
		else:
			return None

	def getWordSenticScore(self, word):
		if word in self.dictionary:
			return self.dictionary[word]
		else:
			return None


	def __init__(self, pathToSN):
		self.dictionary = dict()
		tree = ET.parse(pathToSN)
		root = tree.getroot()
		for child in root:
			text = child[1].text
			sr = SenticScore(float(child[7].text), float(child[8].text), float(child[9].text), float(child[10].text), float(child[11].text))

			self.dictionary[text] = sr