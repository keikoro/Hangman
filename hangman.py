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

if sys.version_info[0] < 3:
    print("You are currently using Python 2.x but need to use Python 3.x to be able to run this game.")
    print("Please start this program by starting your command with python3 or install Python 3 from http://www.python.org if you don't have it installed on your system.")

def stringtogether(thislist):
	"""return elements in a list as a string"""
	returnstring = ""
	for element in thislist:
		returnstring += element
	return returnstring

def output(text,voice=True,ending='\n',spell=False):
	"""print out text and, if voice is true, say text"""
	# say cannot spell single dots/dashes etc. :(	
	print(text,end=ending)
	if voice:
		if spell:
			# if there are more than maxvoicedblanks blanks, don't spell them out (but say "n blank characters")
			speaklist = []
			howmanyblanks = 0
			for char in text:
				if char == placeholderchar:
					howmanyblanks += 1
				else:
					if howmanyblanks > 0:
						# append how many blank characters there are
						if howmanyblanks > maxvoicedblanks:
							speaklist.append("{} {}s ".format(howmanyblanks,placeholdercharvoiced))
						else:
							for x in range(howmanyblanks):
								speaklist.append(placeholdercharvoiced)
					speaklist.append(char)
					howmanyblanks = 0

			if char == placeholderchar: # needed for when last character is a dot
				if howmanyblanks > maxvoicedblanks:
					speaklist.append("{} {}s ".format(howmanyblanks,placeholdercharvoiced))
				else:
					for x in range(howmanyblanks):
						speaklist.append(placeholdercharvoiced)

			for element in speaklist:
				subprocess.call([voicesoftware, element])

		else:
			subprocess.call([voicesoftware, text])


def analysewords(mywords):
	'''analyse mywords and return a list of all used characters (sorted by occurence)'''
	mydict = {}
	for word in mywords: # create dictionary with occurence of letters in all words
		for letter in word.lower():
			if letter in mydict:
				mydict[letter] += 1
			else:
				mydict[letter] = 1

	# list of pairs in mydict dictionary sorted by occurence (descending)
	# adapted from http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value
	pairlist = sorted(mydict.items(), key=lambda x: x[1], reverse=True)
	# pairlist looks like this: [('e', 167410), ('n', 100164),...]
	
	occurencestring = ''
	for pair in pairlist:
		occurencestring += pair[0] # make string out of each 1st element of a pair
	return list(occurencestring.upper())	

def showhint():
	'''returns the first element of occurencelist as text'''
	return str(occurencelist[0])


# ---- start program
maxvoicedblanks = 2
voicesoftware = ''
alphabet = "abcdefghijklmnopqrstuvwxyz"
mywords = [] # empty list
possibletries = 11 # 11 incorrect guesses are allowed
incorrectguesses = '' # string for incorrectly guessed letters
correctguesses = ''
tryword = 'tries'
sound = True
wordlanguage = ''
placeholderchar = '-'
placeholdercharvoiced = 'blank'

# determine the user's OS and choose the corresponding audio/voice software
if sys.platform == 'darwin':
	voicesoftware = 'say'
elif (sys.platform == 'linux') or (sys.platform == 'win32'):
	voicesoftware = 'espeak'
else:
	voicesoftware = 'espeak'

# check if user input any parameters
if len(sys.argv) > 1:
	# begin loop
	argumentlist = sys.argv[1:] # all arguments but the filename (which is the 1st arg)
	for argument in argumentlist:
		thisargument = argument.lower()
		if (thisargument == "-nosound") or (thisargument == "nosound"):
			sound = False
			continue
		if (thisargument == "en") or (thisargument == "-en") or (thisargument == "de") or (thisargument == "-de"):
			if "en" in argumentl:
				if wordlanguage != '':
					print("You entered more than one parameter for language - Hangman will now default to English.")
				wordlanguage = "en"
			else:
				if wordlanguage != '':
					print("You entered more than one parameter for language - Hangman will now default to German.")
				wordlanguage = "de"				

if wordlanguage == '':
	wordlanguage = 'en'

try: # filter out 5+ letter words from dict file
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
except: # fallback list of words in case dict file isn't found
	mywords = ["cherry", "summer", "winter", "programming", "hydrogen", "Saturday",
			"unicorn", "magic", "artichoke", "juice", "hacker", "python", "Neverland",
			"baking", "sherlock", "troll", "batman", "japan", "pastries", "Cairo",
			"Vienna", "raindrop", "waves", "diving", "Malta", "cupcake", "ukulele"]

occurencelist = analysewords(mywords)
theword = random.choice(mywords)
placeholderword = list(placeholderchar*len(theword)) # a list consisting of placeholderword characters

if sound:
	print("Starting soundcheck...")
	# use try to test existence of subprocess for audio output (say or espeak)
	try:
		subprocess.call([voicesoftware, "If you can hear a voice and want to play with audio output, please type yes and press enter. Otherwise type no and press enter."])
	except:
		print("Please install the programm '{}' to use audio output (or have your system administrator install it for you).".format(voicesoftware))
		print("Note that you can still play the text-only version of Hangman even if you don't have '{}' installed!".format(voicesoftware))
		sound = False
	else:
		print("You have the necessary software installed to play Hangman with sound/voice output.".format(voicesoftware))
		print("Could you hear your computer talk and do you want to play with audio enabled?")
		answer = input("Please type yes or no (and press enter): ")
		if len(answer) > 0 and answer.lower()[0] == 'y':
			sound = True
		else:
			sound = False
	finally:
		print("Soundcheck completed, you're ready to play.")

output("Let's play Hangman! You have to guess the word.", voice=sound)
output("Whenever you want the computer to help you, type in a {}.".format("question mark"), voice=sound)

output(stringtogether(placeholderword), voice=False) # show blank word
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
		output("You could try guessing the letter '{}'.".format(showhint()), voice=sound)
		continue		

	if not pickedletter.isalpha() : # don't allow digits, special characters
		output("Sorry, but you didn't type a letter! Try again.".format(pickedletter), voice=sound)
		continue

	if pickedletter in incorrectguesses: # no multiple guesses of same letter
		output("You already guessed the letter '{}'!".format(pickedletter), voice=sound)
		continue

	if pickedletter in correctguesses:
		output("You already successfully picked '{}'!".format(pickedletter.upper()), voice=sound)
		continue

	if pickedletter in theword.upper(): # guess was correct
		
		# replace placeholderword letters with correctly guessed ones
		letterposition = 0
		for letterexists in theword.upper():
			if letterexists == pickedletter:
				placeholderword[letterposition] = theword.upper()[letterposition]
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
			print('.')	
	# ----- end guessing

	# remove pickedletter from hint list occurencelist
	if pickedletter in occurencelist:
		occurencelist.remove(pickedletter)

	if not placeholderchar in placeholderword:
		output("We have a winner! Thanks for playing. :)", voice=sound)
		break

	if placeholderword == list(placeholderchar*len(theword)):
		output(stringtogether(placeholderword), voice=False) # show blank word
		if sound:
			subprocess.call([voicesoftware, "The word you're looking for has {} letters".format(len(theword))])
	else:
		output("The word is: ", ending='', voice=sound)
		output(stringtogether(placeholderword),spell=True, voice=sound)

else:
	output("\nGame over. :( ", voice=sound)

output("The word you were looking for was: " +theword+ '.', voice=sound)
