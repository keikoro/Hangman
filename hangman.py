# A simple hangman game in Python

import random

def stringtogether(mylist):
	for letter in mylist:
		# Liste ausgeben in einer Wurscht
		print(letter,end='')
	print()


mywords = ["marmelade", "testwort", "schal", "sommer", "müsli", "butterbrot", 
				"startrek", "lampe"]

print("Let's play hangman: guess the word!")
myword = random.choice(mywords)

wrongguesses = 0
maxwrongguesses = 11
blankword = list("-"*len(myword))
guessed = ''

while wrongguesses <= maxwrongguesses:
	stringtogether(blankword)

	pickletter = input("Please enter a letter : ")
	pickletter = pickletter.lower()

	guessed += pickletter

	if pickletter in myword:
		print("That guess was correct!")
		
		position = 0

		for letterexists in myword:
			if letterexists == pickletter:
				# Umbau der blankword (ersetze Strich mit buchstabe)
				blankword[position] = myword[position]
			position += 1

	else:
		wrongguesses += 1
		print("Sorry, that was a wrong guess!")

	print("Letters guessed so far:", guessed, ".\nYou have {} tries left".format(maxwrongguesses-wrongguesses))

	if not "-" in blankword:
		print("We have a winner!")
		break

else:
	print("Game over. :( ")

print("Thanks for playing!")
setzezusammen(blankword)
