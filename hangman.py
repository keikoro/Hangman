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
# - retrieve words from a Wikipedia page
# - build hangman (ASCII graphics)
# - transform umlauts (ü -> ue)
# - delay for say? (so as to display text earlier)
# - switch between EN and DE words (dict file) ... parameters!
# - hint system (which letter is likely to be part of the word)
# - alternatives for say for other platforms (linux, windows)
# - AI
# - put licence into comments (check underscore blahfoo)
#
# Further ideas:
# - let user guess the entire word
# - allow phrases and words with hyphens
# - multiplayer hangman

'''Hangman - a word-guessing game.

parameters:
-nosound ... play the game without sound
-en|de ... play the game with English/German words'''

import random # module for randomisation
import subprocess # enable command line functions
import sys # module for parameters

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
			# say cannot say a single underscore/dash/... :( -> needs to be spelled out
			for char in list(text):
				if char == ".":
					subprocess.call(["say", "dot"])
				else:
					subprocess.call(["say", char])
		else:
			subprocess.call(["say", text])

# start of the program

sound = True
wordlanguage = ""
# are there any parameters?
if len(sys.argv) > 1:
	# begin loop
	argumentlist = sys.argv[1:] # list includes all arguments but not the filename
	for argument.lower() in argumentlist:
		if (argument == "-nosound") or (argument == "nosound"):
			sound = False
			continue
		if (argument == "en") or (argument == "-en") or (argument == "de") or (argument == "-de"):
			if "en" in argument:
				if wordlanguage != '':
					print("You entered more than one parameters for language - this is not possible!")
					print("The Hangman program will now default to English.")
				wordlanguage = "en"
			else:
				if wordlanguage != '':
					print("You entered more than one parameters for language - this is not possible!")
					print("The Hangman program will now default to German.")
				wordlanguage = "de"				

if wordlanguage == '':
	wordlanguage = 'en'

alphabet = "abcdefghijklmnopqrstuvwxyz"
mywords = [] # empty list

try:
	myfile = open("de-en.dict")
	for line in myfile:
		myword = line.split()[0]
		for letter in myword.lower():
			if len(myword) < 5:
				break
			if not letter in alphabet:
				break
		else:
			mywords.append(myword)

	myfile.close()
except:
	mywords = ["cherry", "summer", "winter", "programming", "hydrogen", "Saturday",
			"unicorn", "magic", "artichoke", "juice", "hacker", "python", "Neverland",
			"baking", "sherlock", "troll", "batman", "japan", "pastries", "Cairo",
			"Vienna", "raindrop", "waves", "diving", "Malta", "cupcake", "ukulele"]

print(len(mywords))

if sound:
	print("Starting sound check:")
	# using try to test existence of say subprocess
	try:
		subprocess.call(["say", "soundcheck, testing, 1, 2, 3"])
		subprocess.call(["say", "If you hear the voice, please press yes and the enter key."])
	except:
		print("Please install the programm 'say' to use audio output (or contact your system administrator).")
		print("Using this program will still work by the way, only without sound.")
		sound = False
	else:
		print("It seems you have 'say' installed which makes audio output possible.")
		print("Could you hear your computer say 'soundcheck, testing, 1, 2, 3'?")
		answer = input("Please type yes or no (and press enter): ")
		if len(answer) > 0 and answer.lower()[0] == 'y':
			sound = True
		else:
			sound = False
	finally:
		print("Soundcheck completed, you're ready to go!")


output("Let's play hangman: guess the word!", voice=sound)

theword = random.choice(mywords)

possibletries = 11 # 11 incorrect guesses are allowed
placeholder = list("."*len(theword)) # a list consisting of placeholder characters
incorrectguesses = '' # string for incorrectly guessed letters
correctguesses = ''
tryword = 'tries'

output(stringtogether(placeholder), voice=False) # show blank word
if sound:
	subprocess.call(["say", "The word you're looking for has {} letters".format(len(theword))])

while possibletries > 0:

	output("Please pick a letter: ", ending='', voice=sound)
	pickedletter = input().upper()

	if len(pickedletter) > 0:
		pickedletter = pickedletter[0]

	if not pickedletter.isalpha() : # don't allow digits, special characters
		output("Sorry, but that was not a letter! Try again.".format(pickedletter), voice=sound)
		continue

	if pickedletter in incorrectguesses: # no multiple guesses of same letter
		output("You already guessed the letter '{}'!".format(pickedletter), voice=sound)
		continue

	if pickedletter in correctguesses:
		output("You already picked {}!".format(pickedletter.upper()), voice=sound)
		continue

	if pickedletter in theword.upper(): # guess was correct
		
		# replace placeholder letters with correctly guessed ones
		letterposition = 0
		for letterexists in theword.upper():
			if letterexists == pickedletter:
				placeholder[letterposition] = theword.upper()[letterposition]
			letterposition += 1

		output("You guessed correctly, well done!", voice=sound)
		correctguesses += pickedletter

	else: # guess was incorrect
		incorrectguesses += pickedletter			
		possibletries -= 1

		output("Sorry, '{}' is an incorrect guess!".format(pickedletter.upper()), voice=sound)

		if (incorrectguesses != '') and (possibletries > 0):
			if possibletries == 1:
				tryword = 'try' 

			output("You have {} {} left.".format(possibletries,tryword), voice=sound)
			output("Incorrectly guessed letters so far: ", ending='', voice=sound)
			output(incorrectguesses, ending='', spell=True, voice=sound)
			print(".")
			
	if not "." in placeholder:
		output("We have a winner! Thanks for playing. :)", voice=sound)
		break

	if placeholder == list("."*len(theword)):
		output(stringtogether(placeholder), voice=False) # show blank word
		if sound:
			subprocess.call(["say", "The word you're looking for has {} letters".format(len(theword))])
	else:
		output("The word is: ", ending='', voice=sound)
		output(stringtogether(placeholder),spell=True, voice=sound)

else:
	output("\nGame over. :( ", voice=sound)

output("The word you were looking for was: " +theword+ ".", voice=sound)
