import xml.etree.ElementTree as ET
import re

class SenticScore:
	def __init__(self, pleasantness, attention, sensitivity, aptitudem, polarity):
		self.pleasantness = pleasantness
		self.attention = attention
		self.sensitivity = sensitivity
		self.aptitude = aptitude
		self.polarity = polarity
	def add(self, senticScore):
		self.pleasantness = self.pleasantness + senticScore.pleasantness
		self.attention = self.attention + senticScore.attention
		self.sensitivity = self.sensitivity + senticScore.sensitivity
		self.aptitude = self.aptitude + senticScore.aptitude
		self.polarity = self.polarity + senticScore.polarity
	def __str__(self):
		return "pleasantness: " + str(self.pleasantness) + ", attention:" + str(self.attention) + ", sensitivity:" + str(self.sensitivity) + ", aptitude: " + str(self.aptitude)+ ", polarity: " + str(self.polarity)

class SenticNet:
	def getTweetSenticScore(self, tweet):
		tweet = re.sub('[^\w ]',' ',tweet) #remove punctuation
		tweet = re.sub(' +',' ', tweet) #remove double spaces
		tweet = tweet.lower()
		words = tweet.split(" ")
		wordcombos = self.getWordCombinations(words, " ")
		total = SenticScore(0.0, 0.0, 0.0, 0.0)

		for w in wordcombos:
			total.add(self.getWordSenticScore(w))
		return total

	def getWordCombinations(self, wordList, seperator):
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



	def getWordSenticScore(self, word):
		if word in self.dictionary:
			return self.dictionary[word]
		else:
			return SenticScore(0.0, 0.0, 0.0, 0.0)


	def __init__(self, pathToSN):
		self.dictionary = dict()
		tree = ET.parse(pathToSN)
		root = tree.getroot()
		for child in root:
			text = child[1].text
			sr = SenticScore(float(child[7].text), float(child[8].text), float(child[9].text), float(child[10].text), float(child[11].text))

			self.dictionary[text] = sr