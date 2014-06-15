#!/usr/local/bin/python
# coding: utf8

import os
from mpi4py import MPI
import re
import time
import codecs
from analysetweet import analyseTweet, combineResults
from senticnet import *
from sentiwordnet import SentiWordNet
from sasatweets import SasaTweets
from nltktweetclassifier import NLTKTweetClassifier


SIZE = MPI.COMM_WORLD.Get_size()
RANK = MPI.COMM_WORLD.Get_rank()
NAME = MPI.Get_processor_name()
COMM = MPI.COMM_WORLD

if RANK == 0:
	print "Opening config file: config/config.txt"
	f = open('config/config.txt', 'r')
	filename = f.read()

	if filename != "":
		print "Opening twitter logfile: " + filename
		f = codecs.open(filename, "r", "utf-8")
		text = f.read()
		tweetList = text.split("\n")
		tweetList = filter(bool, tweetList)

		print "twitter log file read (" + str(len(tweetList)) +" tweets)"
		print "initializing classifiers..."

		senticNetInstance = SenticNet("res/senticnet2.rdf.xml")
		sentiWordNetInstance = SentiWordNet("res/SentiWordNet_3.0.0_20130122.txt")
		
	else:
		tweetList = None
		sasaInstance = None
		senticNetInstance = None
		sentiWordNetInstance = None
else:
	tweetList = None
	senticNetInstance = None
	sentiWordNetInstance = None

#broadcasting the sasa or nltk analyzer doesn't work! => Initialise it in every process (very bad in terms of performance)
sasaInstance = SasaTweets()
nltkTweetClassifierInstance = NLTKTweetClassifier()

COMM.Barrier()

if RANK == 0:
	print "classifiers initialised..."

#share tweets
tweetList = COMM.bcast(tweetList, root=0)

#share analyzer instances
senticNetInstance = COMM.bcast(senticNetInstance, root=0)
sentiWordNetInstance = COMM.bcast(sentiWordNetInstance, root=0)

if tweetList != None and sasaInstance != None and senticNetInstance != None and sentiWordNetInstance != None and nltkTweetClassifierInstance != None:
	tweetsPerThread = len(tweetList)/SIZE
	resultList = []

	if RANK == 0:
		print "analyzing data..."

	#get indices to process
	if RANK == SIZE-1:
		#last
		startTweet = RANK*tweetsPerThread
		endTweet = len(tweetList)
	else:
		startTweet = RANK * tweetsPerThread
		endTweet = ((RANK + 1) * tweetsPerThread)

	for i in range(startTweet, endTweet):
		tweet = tweetList[i].split("\t")
		resultList.append(analyseTweet(tweet[1], sasaInstance, senticNetInstance, sentiWordNetInstance, nltkTweetClassifierInstance))

	resultList = COMM.gather(resultList, root=0)

	COMM.Barrier()

	if RANK == 0:
		print "analyzing finished...combining & refining results"

		allResults = []

		for rlist in resultList: #result list = list of result lists for every process
			for r in rlist: #r = actual results
				allResults.append(r)

		print "all results len: " + str(len(allResults))
		combineResults(allResults)
else:
	if RANK == 0:
		print "unable to load config"