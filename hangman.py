# A simple hangman game programmed in Python 3
#
# You need to have Python 3 installed on your system to be able to run this game.
# Tested on Python 3.3.2.
#
# The game prompts the user to enter a letter to start guessing a word.
# 11 incorrect guesses are allowed, after the 11th, hangman is hanged and the game is over.
# You can enable/disable audio output (see output function)
#
#
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
			# if there are more than maxdots dots, don't spell them out (but say "n blank characters")
			#if "."*(maxdots+1) in text:
			speaklist = []
			dotstreak = 0
			for char in text:
				if char == ".":
					dotstreak += 1
				else:
					if dotstreak > 0:
						# we must append x times dot
						if dotstreak > maxdots:
							speaklist.append("{} dots ".format(dotstreak))
						else:
							for x in range(dotstreak):
								speaklist.append("dot")
					speaklist.append(char)
					dotstreak = 0

			if char == ".": # needed for if last character is a dot
				if dotstreak > maxdots:
					speaklist.append("{} dots ".format(dotstreak))
				else:
					for x in range(dotstreak):
						speaklist.append("dot")

			for element in speaklist:
				subprocess.call([voicesoftware, element])

			# say cannot say a single underscore/dash/... :( -> needs to be spelled out

		else:
			subprocess.call([voicesoftware, text])


def analysewords(mywords):
	'''analyse mywords and return a sorted list of chars (sorted by occurence)'''
	# occurence of letters in all words
	mydict = {}
	for word in mywords:
		for letter in word.lower():
			if letter in mydict:
				mydict[letter] += 1
			else:
				mydict[letter] = 1

	# list of pairs (in the dictionary) sorted by occurence descending
	# see http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value
	pairlist = sorted(mydict.items(), key=lambda x: x[1], reverse=True)

	# pairlist looks like this: [('e', 167410), ('n', 100164),...]
	occurencestring = ''

	for pair in pairlist:
		occurencestring += pair[0]

	return list(occurencestring.upper())	

def showhint():
	'''returns the first element of occurencelist as text'''
	return str(occurencelist[0])

# start of the program

maxdots = 2
voicesoftware = ''
alphabet = "abcdefghijklmnopqrstuvwxyz"
mywords = [] # empty list
possibletries = 11 # 11 incorrect guesses are allowed
incorrectguesses = '' # string for incorrectly guessed letters
correctguesses = ''
tryword = 'tries'
sound = True
wordlanguage = ''

# check for os/voice software
if sys.platform == 'darwin':
	voicesoftware = 'say'
elif (sys.platform == 'linux') or (sys.platform == 'win32'):
	voicesoftware = 'espeak'
else:
	voicesoftware = 'espeak'

# are there any parameters?
if len(sys.argv) > 1:
	# begin loop
	argumentlist = sys.argv[1:] # list includes all argumentls but not the filename
	for argument in argumentlist:
		argumentl = argument.lower()
		if (argumentl == "-nosound") or (argumentl == "nosound"):
			sound = False
			continue
		if (argumentl == "en") or (argumentl == "-en") or (argumentl == "de") or (argumentl == "-de"):
			if "en" in argumentl:
				if wordlanguage != '':
					print("You entered more than one parameter for language - this is not possible!")
					print("The Hangman program will now default to English.")
				wordlanguage = "en"
			else:
				if wordlanguage != '':
					print("You entered more than one parameter for language - this is not possible!")
					print("The Hangman program will now default to German.")
				wordlanguage = "de"				

if wordlanguage == '':
	wordlanguage = 'en'

try: # get 5+ letter words out of dict file
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

occurencelist = analysewords(mywords)
theword = random.choice(mywords)
placeholder = list("."*len(theword)) # a list consisting of placeholder characters

if sound:
	print("Starting sound check:")
	# using try to test existence of voicesoftware subprocess
	try:
		subprocess.call([voicesoftware, "soundcheck"])
		subprocess.call([voicesoftware, "If you can hear a voice, please type yes (and press enter)."])
	except:
		print("Please install the programm '{}' to use audio output (or contact your system administrator).".format(voicesoftware))
		print("You can use this program even if you don't have '{}' installed (just without sound).".format(voicesoftware))
		sound = False
	else:
		print("It seems you have '{}' installed which makes audio output possible.".format(voicesoftware))
		print("Could you hear your computer say 'soundcheck'?")
		answer = input("Please type yes or no (and press enter): ")
		if len(answer) > 0 and answer.lower()[0] == 'y':
			sound = True
		else:
			sound = False
	finally:
		print("Soundcheck completed, you're ready to go!")

output("Let's play hangman: guess the word!", voice=sound)

output(stringtogether(placeholder), voice=False) # show blank word
if sound:
	subprocess.call([voicesoftware, "The word you're looking for has {} letters".format(len(theword))])

while possibletries > 0:

	output("Please pick a letter: ", ending='', voice=sound)
	pickedletter = input().upper()

	if pickedletter == '???':
		occurencestringpretty = ''
		for char in str(occurencelist):
			if char not in "'[]":
				occurencestringpretty += char

		output("Clever you! The most common letters are: {}".format(occurencestringpretty), voice=sound)
		continue

	if len(pickedletter) > 0:
		pickedletter = pickedletter[0]

	if pickedletter == '?':
		output("You could try the letter {}".format(showhint()), voice=sound)
		continue		

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
	
	# guess done

	# remove pickedletter from hint list occurencelist
	if pickedletter in occurencelist:
		occurencelist.remove(pickedletter)

	if not "." in placeholder:
		output("We have a winner! Thanks for playing. :)", voice=sound)
		break

	if placeholder == list("."*len(theword)):
		output(stringtogether(placeholder), voice=False) # show blank word
		if sound:
			subprocess.call([voicesoftware, "The word you're looking for has {} letters".format(len(theword))])
	else:
		output("The word is: ", ending='', voice=sound)
		output(stringtogether(placeholder),spell=True, voice=sound)

else:
	output("\nGame over. :( ", voice=sound)

output("The word you were looking for was: " +theword+ ".", voice=sound)
