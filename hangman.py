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
# - a letter can't be guessedletters more than once (i.e. only counts toward incorrect guesses once)
# - incorrectly guessedletters letters are continuously displayed (correct guesses are part of word anyway)
# - words can contain uppercase and lowercase letters
#
# TODO
# - retrieve words-to-be-guessedletters from a file (with minimum length of e.g. 5 letters/word)
# - build hangman (ASCII graphics)
# - differentiate between plural & singular form for tries left (5 tries vs. 1 try)
# - adjust countdown of incorrect guesses (currently counts down from 10 to 0)
# - rearrange print statements (reduce lines)
# - output everything with say (= sound)
# - add more comments!
#
# Ideas for additional/advanced Nice To Have's
# - let user guess the entire word
# - allow phrases and words with hyphens

import random # module for randomisation


def stringtogether(thislist):
	for element in thislist:
		# string together all elements in a list (using no separator between elements) 
		print(element,end='')
	print()


mywords = ["Marmelade", "Testwort", "Schal", "Sommer", "Müsli", "Butterbrot", 
				"Startrek", "Lampe"]

print("Let's play hangman: guess the word!")
# randomly pick one of the words from my list of words
theword = random.choice(mywords)

no_incorrectguesses = 0 # in the beginning, the count of wrong guesses is zero
maxno_incorrectguesses = 10 # only 11 incorrect guesses are allowed
blankword = list("-"*len(theword)) # create a "blank" word with the length of theword
guessedletters = '' # all (incorrectly) guessed letters

while no_incorrectguesses <= maxno_incorrectguesses:
	stringtogether(blankword)

	# let user pick a letter
	pickedletter = input("Please pick a letter : ")

	# warn if input is a digit, special character etc.
	if not pickedletter.isalpha() :
		print("Sorry, but {} is not a letter! Try again.".format(pickedletter))

	elif pickedletter in guessedletters:
		print("You already guessed the letter {}!".format(pickedletter))

	else:

		# lowercase all input
		pickedletter = pickedletter.lower()

		if pickedletter in theword.lower():
			print("You guessed correctly - well done!")
			
			letterposition = 0

			for letterexists in theword.lower():
				if letterexists == pickedletter:
					# replace blank spots in word-to-guess with guessedletters letters
					blankword[letterposition] = theword[letterposition]
				letterposition += 1

		else:
			# add wrong letter to string with incorrect guesses
			guessedletters += pickedletter			
			no_incorrectguesses += 1
			print("Sorry, that guess was wrong! Try again.")

		print("Incorrectly guessed letters so far: " +guessedletters+ ".\nYou have {} tries left".format(maxno_incorrectguesses-no_incorrectguesses))

		if not "-" in blankword:
			print("We have a winner! Thanks for playing.")
			break

else:
	print("Game over. :( ")

print("The word we you were looking for was: " +theword+ ".")
