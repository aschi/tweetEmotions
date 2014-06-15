#!/usr/local/bin/python
# coding: utf8

import matplotlib.pyplot as plt
#Label bars of barchart
def autolabel(rects):
    # attach some text labels
    for rect in rects:
    	neg = 1

    	if rect.get_bbox().get_points()[0][1] < 0: #if value < 0 set neg flag
    		neg = -1

        height = rect.get_height()

        if(height > 1):
        	plt.text(rect.get_x()+rect.get_width()/2., neg*1.02*height, '%d'%int(neg*height), ha='center', va='bottom')
        else:
        	plt.text(rect.get_x()+rect.get_width()/2., neg*1.02*height, '%f'%float(neg*height), ha='center', va='bottom')


