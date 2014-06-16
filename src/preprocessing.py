#!/usr/local/bin/python
# coding: utf8

import re

def preprocessTweet(tweet):
	tweet = re.sub('[^\w ]',' ',tweet) #remove punctuation
	tweet = re.sub(' +',' ', tweet) #remove double spaces
	tweet = tweet.lower()
	words = tweet.split(" ")
	return words

def getWordCombinations(wordList, seperator):
	comboList = []
	for i in range(len(wordList)):
		wordcombo = ""
		for n in range(i, len(wordList)):
			if(wordcombo == ""):
				wordcombo = wordList[n]
			else:
				wordcombo = wordcombo + seperator +wordList[n]
			comboList.append(wordcombo)
	return comboList