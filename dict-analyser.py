alphabet = "abcdefghijklmnopqrstuvwxyz" # allowed characters
goodwords = [] # empty list

myfile = open("de-en.dict")

for line in myfile:
	myword = line.split()[0]
	for letter in myword.lower():
		if len(myword) < 5: # only use words that are at least 5 characters long
			break
		if not letter in alphabet:
			break
	else:
		goodwords.append(myword)

myfile.close()

# create dictionary with occurence of letters in all words
mydict = {}
for word in goodwords:
	for letter in word.lower():
		if letter in mydict:
			mydict[letter] += 1
		else:
			mydict[letter] = 1

# list of pairs (in the dictionary) sorted by occurence (descending)
# adapted from http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value
pairlist = sorted(mydict.items(), key=lambda x: x[1], reverse=True)
# pairlist looks like this: [('e', 167410), ('n', 100164),...]
occurencestring = ''

for pair in pairlist:
	occurencestring += pair[0]

tiplist = list(occurencestring)
print(tiplist)
