#!/usr/local/bin/python
# coding: utf8

import os
from mpi4py import MPI
import re
import time
import codecs
from analyse_tweet import analyseTweet, combineResults
from senticnet import *
from sentiwordnet import SentiWordNet
from sasa_tweet_classifier import SasaTweetClassifier
from nltk_tweet_classifier import NLTKTweetClassifier
from logger import Logger


SIZE = MPI.COMM_WORLD.Get_size()
RANK = MPI.COMM_WORLD.Get_rank()
NAME = MPI.Get_processor_name()
COMM = MPI.COMM_WORLD

if RANK == 0:
	log = Logger("logs/log_" + str(int(time.time()))+".txt")
	log.log("MPI.COMM_WORLD.Get_size(): " + str(SIZE))
	totalTime = time.time()
	lapTime = time.time()
	log.log("Opening config file: config/config.txt")
	f = open('config/config.txt', 'r')
	config = f.read()
	config = config.split("#-#-#-#")
	filename = config[0]
	title = config[1]
	
	title_file_prefix = title.lower()
	title_file_prefix = re.sub('[^\w ]',' ',title_file_prefix) #remove punctuation
	title_file_prefix = re.sub(' +',' ', title_file_prefix) #remove double spaces
	tmp = title_file_prefix.split(" ")
	title_file_prefix = "_".join(tmp)

	log.log("Config read (title: " + title + "; filename: " + filename + ") [" + str((time.time()-lapTime)) +"s]")

	if filename != "" and title_file_prefix != "":
		lapTime = time.time()
		log.log("Opening twitter logfile: " + filename)
		f = codecs.open(filename, "r", "utf-8")
		text = f.read()
		tweetList = text.split("\n")
		tweetList = filter(bool, tweetList)

		log.log("twitter log file read (" + str(len(tweetList)) +" tweets) [" + str((time.time()-lapTime)) +"s]")
		lapTime = time.time()
		log.log("initializing classifiers...")

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
sasaInstance = SasaTweetClassifier()
nltkTweetClassifierInstance = NLTKTweetClassifier()

COMM.Barrier()

if RANK == 0:
	log.log("classifiers initialised... [" + str((time.time()-lapTime)) +"s]")

#share tweets
tweetList = COMM.bcast(tweetList, root=0)

#share analyzer instances
senticNetInstance = COMM.bcast(senticNetInstance, root=0)
sentiWordNetInstance = COMM.bcast(sentiWordNetInstance, root=0)

if tweetList != None and sasaInstance != None and senticNetInstance != None and sentiWordNetInstance != None and nltkTweetClassifierInstance != None:
	tweetsPerThread = len(tweetList)/SIZE
	resultList = []

	if RANK == 0:
		lapTime = time.time()
		log.log("analyzing data...")

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
		log.log("analyzing finished... [" + str((time.time()-lapTime)) +"s]")
		lapTime = time.time()
		log.log("combining & refining results...")

		allResults = []

		for rlist in resultList: #result list = list of result lists for every process
			for r in rlist: #r = actual results
				allResults.append(r)

		combineResults(allResults, title_file_prefix, log)
		log.log("done [" + str((time.time()-lapTime)) +"s]")
		log.log("total time used: "+ str((time.time()-totalTime)) +"s")
else:
	if RANK == 0:
		log.log("unable to load config")
		log.log("total time used: "+ str((time.time()-totalTime)) +"s")