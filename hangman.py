# A simple hangman game programmed in Python 3
#
# You need to have Python 3 installed on your system to be able to run this game.
# Tested on Python 3.3.2.
#
# The game prompts the user to enter a letter to start guessing a word.
# 11 incorrect guesses are allowed, after the 11th, hangman is hanged and the game is over.
# You can enable/disable audio output (see output function)
#
# TODO
# - retrieve words-to-be-guessed from a file (with minimum length of e.g. 5 letters/word)
# - build hangman (ASCII graphics)
# - voice output for placeholder word (problem with placeholder characters)
# - fix voice problem with apostrophes
#
# Further ideas:
# - let user guess the entire word
# - allow phrases and words with hyphens

import random # module for randomisation
import subprocess # enable command line functions

def stringtogether(thislist): # function to string together elements in a list
	for element in thislist:
		print(element,end='')
	print()

def output(text,voice=True):
	# set voice to 'true' to enable audio output
	if voice:
		subprocess.call(["say", text])
		#system('say -r 160 %s' % (text))		

mywords = ["cherry", "summer", "winter", "programming", "hydrogen", "Saturday",
			"unicorn", "magic", "artichoke", "juice", "hacker", "python", "Neverland",
			"baking", "sherlock", "troll", "batman", "japan", "pastries", "Cairo",
			"Vienna", "raindrop", "waves", "diving", "Malta", "cupcake", "ukulele"]

text = "Let us play hangman: guess the word!"
output(text)

theword = random.choice(mywords).upper()

possibletries = 11 # 11 incorrect guesses are allowed
placeholder = list("_"*len(theword)) # a list consisting of placeholder characters
incorrectguesses = '' # string for incorrectly guessed letters
correctguesses = ''
tryword = 'tries'

stringtogether(placeholder) # show blank word

while possibletries > 0:

	text = "Please pick a letter: "
	output(text)
	pickedletter = input()

	if not pickedletter.isalpha() : # don't allow digits, special characters
		text = "Sorry, but that was not a letter! Try again.".format(pickedletter)
		output(text)

	elif pickedletter.upper() in incorrectguesses: # no multiple guesses of same letter
		text = "You already guessed the letter '{}'!".format(pickedletter.upper())
		output(text)

	else:
		pickedletter = pickedletter.upper() # uppercase all input (better for say)

		if (pickedletter in theword.upper()) and (pickedletter not in correctguesses):
			
			# replace placeholder letters with correctly guessed ones
			letterposition = 0
			for letterexists in theword.upper():
				if letterexists == pickedletter:
					placeholder[letterposition] = theword[letterposition]
				letterposition += 1

			stringtogether(placeholder)
			correctguesses += pickedletter

			text = "You guessed correctly, well done!"
			output(text)

		elif pickedletter in correctguesses:
			text = "You already picked {}!".format(pickedletter.upper())
			output(text)

		else:
			# add incorrect letters to incorrectguesses
			incorrectguesses += pickedletter			
			possibletries -= 1

			text="Sorry, '{}' is an incorrect guess!".format(pickedletter.upper())
			output(text)

			if (incorrectguesses != '') and (possibletries > 0):
				if possibletries == 1:
					tryword = 'try' 

				text = "You have {} {} left.".format(possibletries,tryword)
				output(text)
				text = "Incorrectly guessed letters so far: " +incorrectguesses+ "."
				output(text)

				stringtogether(placeholder)

		if not "-" in placeholder:
			text = "We have a winner! Thanks for playing. :)"
			output(text)
			break

else:
	text = "\nGame over. :( "
	output(text)

text = "The word we you were looking for was: " +theword+ "."
output(text)
