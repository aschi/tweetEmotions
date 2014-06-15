#!/usr/local/bin/python
# coding: utf8

import requests
import urllib2
import json

def analyzeTweet(tweet):
	encTweet = urllib2.quote(tweet.encode("utf8"))
	
	payload = {'text': encTweet}
	r = requests.post("http://text-processing.com/api/sentiment/", data=payload)
	return json.loads(r.text)