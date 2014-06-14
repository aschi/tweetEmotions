from sasa.classifier import Classifier

class SasaTweets:
	def classifyTweet(self, tweet):
		return self.c.classifyFromText(tweet)

	def __init__(self):
		self.c = Classifier()