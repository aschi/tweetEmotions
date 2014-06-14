import sys
import os
sys.path.insert(0, '../lib/TwitterSearch/')
from TwitterSearch import *
from mpi4py import MPI
import numpy as np
import re
import time
import codecs
from analysetweet import analysetweet
from is_number import is_number

SIZE = MPI.COMM_WORLD.Get_size()
RANK = MPI.COMM_WORLD.Get_rank()
NAME = MPI.Get_processor_name()
COMM = MPI.COMM_WORLD

if RANK == 0:
	filename = ""

	inputVar = raw_input("Do you have a twitter logfile or would you like to gather new data?: (e = existing, n = new data (default))")
	if(inputVar == "e"):
		inputVar = raw_input("Please enter the filename (relative to the scripts path!):")
		filename = inputVar
	else:
		inputVar = raw_input("Enter serach terms (seperated by space):")
		inputVar = re.sub(' +',' ', inputVar) #remove double spaces
		inputWords = inputVar.split(" ")

		fn = ""
		disp = ""
		for w in inputWords:
			if disp == "":
				disp = "'"+w+"'"
				fn = w
			else:
				disp = disp+", '"+w+"'"
				fn = fn + "_" + w

		print("You entered [" + disp+ "]")  

		inputVar = raw_input("Would you like to start fetching tweets? This can only be done once per hour! (y/n default is n):")
		inputVar = inputVar.lower()
		if inputVar == "y" or inputVar == "yes" or inputVar == "j" or inputVar == "ja":
			try:
				tso = TwitterSearchOrder() # create a TwitterSearchOrder object
				inputWords.append("-RT") #Filter retweets
				tso.setKeywords(inputWords) # let's define all words we would like to have a look for
				tso.setLanguage('en') # we want to see German tweets only
				#tso.setCount(noTweets) # please dear Mr Twitter, only give us 7 results per page
				tso.setIncludeEntities(False) # and don't give us all those entity information
				
				ts = TwitterSearch(consumer_key = 'LI7bi7oui3FFUXHCSGcw',consumer_secret = 'QCBmNKVSXvkt7ioU4TQaf6XVL9pKBifD8ch3zQvY',access_token = '2353654315-7LkOG9CFFUewoeIezPloEEY2vHmpE0Mo8vFhkkB',access_token_secret = 'XKyVTRLQB9jDTlXteQbsoULKTqdI6w79IP3HokVI9R1Iu')
				
				filename = "data/"+fn + '_raw_search_' + str(time.time()) +".txt"
				f = open(filename, 'w')

				for tweet in ts.searchTweetsIterable(tso): # this is where the fun actually starts :)
					text = tweet['user']['screen_name'] + "\t" + tweet['text']
					textList = text.splitlines()
					text = " ".join(textList)
					text = text + "\n"
					f.write(text.encode('utf8'))

					print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
				f.close()
				print "tweets saved to: " + filename
			except TwitterSearchException as e: # take care of all those ugly errors if there are some
				print(e)
	f = codecs.open(filename, "r", "utf-8")
	text = f.read()
	tweetList = text.split("\n")
else:
	tweetList = None

tweetList = COMM.bcast(tweetList, root=0)
tweetsPerThread = len(tweetList)/SIZE
resultList = []

#get indices to process
if RANK == SIZE-1:
	#last
	startTweet = RANK*tweetsPerThread
	endTweet = len(m1)
else:
	startTweet = RANK * tweetsPerThread
	endTweet = ((RANK + 1) * tweetsPerThread)

for i in range(startTweet, endTweet):
	resultList.append(analysetweet(tweetList[i]))
