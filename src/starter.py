#!/usr/local/bin/python
# coding: utf8

import os
from gather_twitterdata import gatherTwitterData

filename = ""
title = ""
inputVar = ""

while inputVar == "":
	inputVar = raw_input("Please enter a title for your twitter analysis: ")
title = inputVar

inputVar = raw_input("Do you have a twitter logfile or would you like to gather new data? (e = existing, n = new data (default)):")
if(inputVar == "e"):
	inputVar = raw_input("Please enter the filename (relative to the scripts path!):")
	filename = inputVar
else:
	filename = gatherTwitterData()

inputVar = raw_input("Do you want to analyse the given data? (" + filename + ")? (y, n = default):")
inputVar = inputVar.lower()
if(inputVar == "yes" or inputVar == "y" or inputVar == "j" or inputVar == "ja"):
	f = open('config/config.txt', 'w')
	f.write(filename + "#-#-#-#" + title)
	f.close()

	os.system("mpiexec -n 2 python analyse_twitterdata.py")