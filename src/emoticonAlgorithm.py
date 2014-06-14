#!/usr/local/bin/python
# coding: utf8

def emoticonAlgorithm(input):
	positive = [":)", ":D", ":-D", ":]", ":}", ":o)", ":o]", ":o}", ":-]", ":-)", ":-}", "=)", "=]", "=}", "=^]", "=^)", "=^}", ":B", ":-D", ":-B", ":^D", ":^B", "=B", "=^B", "=^D", ":’)", ":’]", ":’}", "=’)", "=’]", "=’}", "<3", "^.^", "^-^", "^_^", "^^", ":*", "=*", ":-*", ";)", ";]", ";}", ":-p", ":-P", ":-b", ":^p", ":^P", ":^b", "=P", "=p", "/o/", ":P", ":p", ":b", "=b", "=^p", "=^P", "=^b", "\o/"]
	negative = ["D:", "D=", "D-:", "D^:", "D^=", ":(", ":[", ":{", ":o(", ":o[", ":^(", ":^[", ":^{", "=^(", "=^{", ">=(", ">=[", ">={", ">=(", ">:-{", ">:-[", ">:-(", ">=^[", ">:-(", ":-[", ":-(", "=(", "=[", "={", "=^[", ">:-=(", ">=[", ">=^(", ":’(", ":’[", ":’{", "=’{", "=’(", "=’[", "=\\", ":\\", "=/", ":/", "=$", "o.O", "O_o", "Oo" ":$:-{", ">:-{", ">=^{", ":o{"]
	neutral = [":|", "=|", ":-|", ">.<", "><", ">_<", ":o", ":0", "=O", ":@", "=@", ":^o", ":^@", "-.-", "-.-’", "-_-", "-_-’", ":x", "=X", ":\#", "=#", ":-x", ":-@", ":-#", ":^x", ":^#"]

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
			return "positive"
		elif pCount == negCount:
			return "neutral"
		else:
			return "negative"
	elif negCount > 0:
		return "negative"

	elif neuCount >0:
		return "neutral"

	return "n/a"
