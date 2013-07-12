# A simple hangman game programmed in Python 3
#
# You need to have Python 3 installed on your system to be able to run this game.
# Tested on Python 3.3.2.
#
# The game prompts the user to enter a letter to start guessing a word.
# 11 incorrect guesses are allowed, after the 11th, hangman is hanged and the game is over.
# 
# Features/checks already implemented
# - only letters are allowed (no digits, no special characters)
# - a letter can't be guessed more than once (i.e. only counts toward incorrect guesses once)
# - incorrectly guessed letters are continuously displayed (correct guesses are part of word anyway)
# - words can contain uppercase and lowercase letters
#
# TODO
# - retrieve words-to-be-guessed from a file (with minimum length of e.g. 5 letters/word)
# - build hangman (ASCII graphics)
# - differentiate between plural & singular form for tries left (5 tries vs. 1 try)
# - adjust countdown of incorrect guesses (currently counts down from 10 to 0)
# - rearrange print statements (reduce lines)
# - output everything with say (= sound)
# - add more comments!
#
# Ideas for additional/advanced Nice To Have's
# - let user guess the entire word


import random

def stringtogether(mylist):
	for letter in mylist:
		# string together list elements
		print(letter,end='')
	print()


mywords = ["Marmelade", "Testwort", "Schal", "Sommer", "Müsli", "Butterbrot", 
				"Startrek", "Lampe"]

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

		if pickletter in myword.lower():
			print("That guess was correct!")
			
			position = 0

			for letterexists in myword.lower():
				if letterexists == pickletter:
					# replace blank spots in word-to-guess with guessed letters
					blankword[position] = myword[position]
				position += 1

		else:
			# add wrong letter to string with incorrect guesses
			guessed += pickletter			
			wrongguesses += 1
			print("Sorry, that was a wrong guess!")

		print("Incorrectly guessed letters so far: " +guessed+ ".\nYou have {} tries left".format(maxwrongguesses-wrongguesses))

		if not "-" in blankword:
			print("We have a winner!")
			break

else:
	print("Game over. :( ")

print("Thanks for playing!")
stringtogether(blankword)
