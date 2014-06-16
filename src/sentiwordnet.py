#!/usr/local/bin/python
# coding: utf8

import os
import re
from preprocessing import preprocessTweet, getWordCombinations

class SentiWordNet:
	def getTweetScore(self, tweet):
		words = preprocessTweet(tweet)
		wordcombos = getWordCombinations(words, "_")
		total = 0.0
		count = 0
		for w in wordcombos:
			ret = self.getWordScore(w)
			if(ret != None):
				total = total + ret
				count = count + 1

		if(count > 0):
			#calculate average
			average = total/count
			return average
		else:
			return None


	def getWordScore(self, word):
		if word in self.dictionary:
			return self.dictionary[word]
		else:
			return None

	def __init__(self, pathToSWN):
		self.dictionary = dict()
		tmpDict = dict()
		f = open(pathToSWN, 'r')
		lineNo = 0
		for line in f:
			lineNo = lineNo+1
			if(line[0] != '#'):
				data = re.split(r'\t+', line)
				if(len(data) != 6):
					raise ValueError("invalid line in senti word net file! (line" + str(lineNo) + "; data length:" + str(len(data)))
				synsetScore = float(data[2])-float(data[3])
				synTerms = data[4].split(" ")
				for st in synTerms:
					stAndRank = st.split("#")
					synTermRank = int(stAndRank[1])
					synTerm = stAndRank[0]

					if not synTerm in tmpDict:
						tmpDict[synTerm] = dict()
					tmpDict[synTerm][synTermRank] = synsetScore
		for entry in tmpDict:
			# Calculate weighted average. Weigh the synsets according to
			# their rank.
			# Score= 1/2*first + 1/3*second + 1/4*third ..... etc.
			# Sum = 1/1 + 1/2 + 1/3 ...
			score = 0.0
			total = 0.0
			for rank in tmpDict[entry]:
				score = score + (float(tmpDict[entry][rank])/float(rank))
				total = total + 1.0 / float(rank)
			score = score / total
			self.dictionary[entry] = score
