import re
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from preprocessing import preprocessTweet
 
class NLTKTweetClassifier:
	def word_feats(self, words):
	    return dict([(word, True) for word in words])

	def classifyTweet(self, tweet):
		words = preprocessTweet(tweet)
		return self.classifier.classify(self.word_feats(words))

	def __init__(self):
		negids = movie_reviews.fileids('neg')
		posids = movie_reviews.fileids('pos')
		 
		negfeats = [(self.word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
		posfeats = [(self.word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
	 
		negcutoff = len(negfeats)*3/4
		poscutoff = len(posfeats)*3/4
	 
		trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
		testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
		#print 'NLTK Classifier init: train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
	 
		self.classifier = NaiveBayesClassifier.train(trainfeats)
		#print 'NLTK Classifier init: accuracy:', nltk.classify.util.accuracy(self.classifier, testfeats)