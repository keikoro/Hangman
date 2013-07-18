# TODO

# 1. wort aus de-en rausextrahieren

# für D- wort: anfang der zeile, wort mit mind 5 buchstaben
# für EN-wort: wort ab ":: ", auch mit mind. 5 buchstaben
# kommentierte zeilen ignorieren

def analysewords(wordlist):
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	goodwords = [] # empty list

	myfile = open("de-en.dict")
	for line in myfile:
		myword = line.split()[0]
		for letter in myword.lower():
			if len(myword) < 5:
				break
			if not letter in alphabet:
				break
		else:
			goodwords.append(myword)

	myfile.close()

	# occurence of letters in all words
	d = {}
	for word in goodwords:
		for letter in word.lower():
			if letter in d:
				d[letter] += 1
			else:
				d[letter] = 1

	# list of pairs (in the dictionary) sorted by occurence descending
	pairlist = sorted(d.items(), key=lambda x: x[1], reverse=True)

	# pairlist looks like this: [('e', 167410), ('n', 100164),...]
	occurencestring = ''

	for pair in pairlist:
		occurencestring += pair[0]

	tiplist = list(occurencestring)
