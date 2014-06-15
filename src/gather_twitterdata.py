#!/usr/local/bin/python
# coding: utf8

import re
import sys
from TwitterSearch import *
import time

def gatherTwitterData():
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
			return filename
		except TwitterSearchException as e: # take care of all those ugly errors if there are some
			print(e)
			return ""