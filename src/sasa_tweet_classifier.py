#!/usr/local/bin/python
# coding: utf8

from sasa.classifier import Classifier

class SasaTweetClassifier:
	def classifyTweet(self, tweet):
		return self.c.classifyFromText(tweet)

	def __init__(self):
		self.c = Classifier()