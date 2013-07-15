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
# - umlauts are two letters!
#
# Further ideas:
# - let user guess the entire word
# - allow phrases and words with hyphens

import random # module for randomisation
import subprocess # enable command line functions

def stringtogether(thislist):
	"""return elements in a list as string"""
	returnstring = ""
	for element in thislist:
		returnstring += element
	return returnstring

def output(text,voice=True,ending='\n',spell=False):
	"""print out text and if voice is true, say text"""
	print(text,end=ending)
	if voice:
		if spell:
			# say cannot say a single underscore/dash/... :(
			for char in list(text):
				if char == ".":
					subprocess.call(["say", "dot"])
				else:
					subprocess.call(["say", char])
		else:
			subprocess.call(["say", text])

mywords = ["cherry", "summer", "winter", "programming", "hydrogen", "Saturday",
			"unicorn", "magic", "artichoke", "juice", "hacker", "python", "Neverland",
			"baking", "sherlock", "troll", "batman", "japan", "pastries", "Cairo",
			"Vienna", "raindrop", "waves", "diving", "Malta", "cupcake", "ukulele"]

greeting = "Let's play hangman: guess the word!"
output(greeting)

theword = random.choice(mywords).upper()

possibletries = 11 # 11 incorrect guesses are allowed
placeholder = list("."*len(theword)) # a list consisting of placeholder characters
incorrectguesses = '' # string for incorrectly guessed letters
correctguesses = ''
tryword = 'tries'

output(stringtogether(placeholder), voice=False) # show blank word
subprocess.call(["say", "The word you're looking for has {} letters".format(len(theword))])

while possibletries > 0:

	output("Please pick a letter: ", ending='')
	pickedletter = input().upper()

	if not pickedletter.isalpha() : # don't allow digits, special characters
		output("Sorry, but that was not a letter! Try again.".format(pickedletter))
		continue

	if pickedletter in incorrectguesses: # no multiple guesses of same letter
		output("You already guessed the letter '{}'!".format(pickedletter))
		continue

	if pickedletter in correctguesses:
		output("You already picked {}!".format(pickedletter.upper()))
		continue

	if pickedletter in theword.upper(): # guess was correct
		
		# replace placeholder letters with correctly guessed ones
		letterposition = 0
		for letterexists in theword.upper():
			if letterexists == pickedletter:
				placeholder[letterposition] = theword[letterposition]
			letterposition += 1

		output("You guessed correctly, well done!")
		correctguesses += pickedletter

	else: # guess was incorrect
		incorrectguesses += pickedletter			
		possibletries -= 1

		output("Sorry, '{}' is an incorrect guess!".format(pickedletter.upper()))

		if (incorrectguesses != '') and (possibletries > 0):
			if possibletries == 1:
				tryword = 'try' 

			output("You have {} {} left.".format(possibletries,tryword))
			output("Incorrectly guessed letters so far: ", ending='')
			output(incorrectguesses, ending='', spell=True)
			print(".")
			
	if not "." in placeholder:
		output("We have a winner! Thanks for playing. :)")
		break

	if placeholder == list("."*len(theword)):
		output(stringtogether(placeholder), voice=False) # show blank word
		subprocess.call(["say", "The word you're looking for has {} letters".format(len(theword))])
	else:
		output("The word is: ", ending='')
		output(stringtogether(placeholder),spell=True)

else:
	output("\nGame over. :( ")

output("The word you were looking for was: " +theword+ ".")
