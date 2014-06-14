import os
import re

class SentiWordNet:
	def getTweetScore(self, tweet):
		tweet = re.sub('[^\w ]',' ',tweet) #remove punctuation
		tweet = re.sub(' +',' ', tweet) #remove double spaces
		tweet = tweet.lower()
		words = tweet.split(" ")
		wordcombos = self.getWordCombinations(words, "_")
		total = 0.0
		for w in words:
			total = total + self.getWordScore(w)
		return total


	def getWordScore(self, word):
		if word in self.dictionary:
			return self.dictionary[word]
		else:
			return 0

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
