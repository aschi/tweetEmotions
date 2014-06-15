#!/usr/local/bin/python
# coding: utf8

import os
from gathertwitterdata import gatherTwitterData

filename = ""

inputVar = raw_input("Do you have a twitter logfile or would you like to gather new data?: (e = existing, n = new data (default))")
if(inputVar == "e"):
	inputVar = raw_input("Please enter the filename (relative to the scripts path!):")
	filename = inputVar
else:
	filename = gatherTwitterData()

inputVar = raw_input("Do you want to analyse the given data? (" + filename + ")? (y = default, n):")
inputVar = inputVar.lower()
if(inputVar == "yes" or inputVar == "y" or inputVar == "j" or inputVar == "ja"):
	f = open('config/config.txt', 'w')
	f.write(filename)
	f.close()

	os.system("mpiexec -n 4 python analyseTwitterdata.py")