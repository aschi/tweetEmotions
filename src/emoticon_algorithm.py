#!/usr/local/bin/python
# coding: utf8

def emoticonAlgorithm(input):
	positive = [u'\u263B', u'\263A', u':)', u':D', u':-D', u':]', u':}', u':o)', u':o]', u':o}', u':-]', u':-)', u':-}', u'=)', u'=]', u'=}', u'=^]', u'=^)', u'=^}', u':B', u':-D', u':-B', u':^D', u':^B', u'=B', u'=^B', u'=^D', u':’)', u':’]', u':’}', u'=’)', u'=’]', u'=’}', u'<3', u'^.^', u'^-^', u'^_^', u'^^', u':*', u'=*', u':-*', u';)', u';]', u';}', u':-p', u':-P', u':-b', u':^p', u':^P', u':^b', u'=P', u'=p', u'/o/', u':P', u':p', u':b', u'=b', u'=^p', u'=^P', u'=^b', u'\o/']
	negative = [u'\u2639',u'D:', u'D=', u'D-:', u'D^:', u'D^=', u':(', u':[', u':{', u':o(', u':o[', u':^(', u':^[', u':^{', u'=^(', u'=^{', u'>=(', u'>=[', u'>={', u'>=(', u'>:-{', u'>:-[', u'>:-(', u'>=^[', u'>:-(', u':-[', u':-(', u'=(', u'=[', u'={', u'=^[', u'>:-=(', u'>=[', u'>=^(', u':’(', u':’[', u':’{', u'=’{', u'=’(', u'=’[', u'=\\', u':\\', u'=/', u'=$', u'o.O', u'O_o', u'Oo', u':$:-{', u'>:-{', u'>=^{', u':o{']
	neutral = [u':|', u'=|', u':-|', u'>.<', u'><', u'>_<', u':o', u':0', u'=O', u':@', u'=@', u':^o', u':^@', u'-.-', u'-.-’', u'-_-', u'-_-’', u':x', u'=X', u':-x', u':-@', u':-#', u':^x']
	pCount = 0
	negCount = 0
	neuCount = 0

	for p in positive:
		if input.find(p) != -1:
			pCount = pCount + input.count(p)

	for neg in negative:
		if input.find(neg) != -1:
			negCount = negCount + input.count(neg)

	for neu in neutral:
		if input.find(neu) != -1:
			neuCount = neuCount + input.count(neu)

	if pCount > 0:
		if pCount > negCount:
			return 'positive'
		elif pCount == negCount:
			return 'neutral'
		else:
			return 'negative'
	elif negCount > 0:
		return 'negative'

	elif neuCount >0:
		return 'neutral'

	return 'n/a'
