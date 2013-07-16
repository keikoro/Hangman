# TODO

# 1. wort aus de-en rausextrahieren

# für D- wort: anfang der zeile, wort mit mind 5 buchstaben
# für EN-wort: wort ab ":: ", auch mit mind. 5 buchstaben
# kommentierte zeilen ignorieren

alphabet = "abcdefghijklmnopqrstuvwxyz"
goodwords = [] # empty list

myfile = open("de-en.txt")
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

d = {}

for word in goodwords:
	for letter in word.lower():
		if letter in d:
			d[letter] += 1
		else:
			d[letter] = 1

print(d)		
