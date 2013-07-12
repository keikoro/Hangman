# A simple hangman game in Python

# Additional features
#
# DONE
# - warning if there's non-letter input
# - warning if letter was already previously guessed
#
# TODO
# 
# - get words-to-be-guessed from a file
# - hangman (graphics)
# - correct guesses needn't be in list of all guesses
# - letter matching should ignore upper/lowercase

import random

def stringtogether(mylist):
	for letter in mylist:
		# string together list elements
		print(letter,end='')
	print()


mywords = ["Marmelade", "Testwort", "Schal", "Sommer", "müsli", "butterbrot", 
				"startrek", "lampe"]

print("Let's play hangman: guess the word!")
myword = random.choice(mywords)

wrongguesses = 0
maxwrongguesses = 11
blankword = list("-"*len(myword))
guessed = ''

while wrongguesses <= maxwrongguesses:
	stringtogether(blankword)

	# let user pick a letter
	pickletter = input("Please pick a letter : ")

	# warn if input is a digit, special character etc.
	if not pickletter.isalpha() :
		print("Sorry, but {} is not a letter!".format(pickletter))

	elif pickletter in guessed:
		print("You already guessed the letter {}!".format(pickletter))

	else:

		# lowercase all input
		pickletter = pickletter.lower()

		# add letter to guessed letters string
		guessed += pickletter

		if pickletter in myword:
			print("That guess was correct!")
			
			position = 0

			for letterexists in myword:
				if letterexists == pickletter:
					# replace blank spots in word-to-guess with guessed letters
					blankword[position] = myword[position]
				position += 1

		else:
			wrongguesses += 1
			print("Sorry, that was a wrong guess!")

		print("Letters guessed so far: " +guessed+ ".\nYou have {} tries left".format(maxwrongguesses-wrongguesses))

		if not "-" in blankword:
			print("We have a winner!")
			break

else:
	print("Game over. :( ")

print("Thanks for playing!")
setzezusammen(blankword)
