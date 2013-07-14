# A simple hangman game programmed in Python 3
#
# You need to have Python 3 installed on your system to be able to run this game.
# Tested on Python 3.3.2.
#
# The game prompts the user to enter a letter to start guessing a word.
# 11 incorrect guesses are allowed, after the 11th, hangman is hanged and the game is over.
#
# TODO
# - retrieve words-to-be-guessed from a file (with minimum length of e.g. 5 letters/word)
# - build hangman (ASCII graphics)
# - output everything with say (= sound)
#
# Further ideas:
# - let user guess the entire word
# - allow phrases and words with hyphens

import random # module for randomisation
from os import system

def stringtogether(thislist): # function to string together elements in a list
	for element in thislist:
		print(element,end='')
	print()

mywords = ["cherry", "summer", "winter", "programming", "hydrogen", "Saturday",
			"unicorn", "magic", "artichoke", "juice", "hacker", "python", "Neverland",
			"baking", "sherlock", "troll", "batman", "japan", "pastries", "Cairo",
			"Vienna", "raindrop", "waves", "diving", "Malta", "cupcake", "ukulele"]

text = "Let us play hangman: guess the word!"
system('say %s' % (text))

theword = random.choice(mywords)

possibletries = 11 # 11 incorrect guesses are allowed
placeholder = list("-"*len(theword)) # a list consisting of placeholder characters
guessedletters = '' # string for incorrectly guessed letters
tryword = 'tries'

stringtogether(placeholder) # show blank word

while possibletries > 0:

	text = "Please pick a letter: "
	system('say %s' % (text))
	pickedletter = input(text)

	if not pickedletter.isalpha() : # don't allow digits, special characters
		text = "Sorry, but that was not a letter! Try again.".format(pickedletter)
		print(text)
		system('say %s' % (text))


	elif pickedletter in guessedletters: # no multiple guesses of same letter
		text = "You already guessed the letter '{}'!".format(pickedletter)
		print(text)
		system('say %s' % (text))

	else:
		pickedletter = pickedletter.lower() # lowercase all input

		if pickedletter in theword.lower():
			
			# replace placeholder letters with correctly guessed ones
			letterposition = 0
			for letterexists in theword.lower():
				if letterexists == pickedletter:
					placeholder[letterposition] = theword[letterposition]
				letterposition += 1

			stringtogether(placeholder)	
			text = "You guessed correctly, well done!"
			system('say %s' % (text))

		else:
			# add incorrect letters to guessedletters
			guessedletters += pickedletter			
			possibletries -= 1

			text="Sorry, '{}' was an incorrect guess!".format(pickedletter)
			print(text, end=' ')
			system('say %s' % (text))

			if (guessedletters != '') and (possibletries > 0):
				if possibletries == 1:
					tryword = 'try' 

				text = "You have {} {} left.".format(possibletries,tryword)
				text2 = "Incorrectly guessed letters so far: " +guessedletters+ "."
				print(text+ "\n" +text2)
				system('say %s' % (text))
				system('say %s' % (text2))
				stringtogether(placeholder)

		if not "-" in placeholder:
			text = "We have a winner! Thanks for playing. :)"
			print(text)
			system('say %s' % (text))
			break

else:
	text = "\nGame over. :( "
	print(text)
	system('say %s' % (text))

text = "The word we you were looking for was: " +theword+ "."
print(text)
system('say %s' % (text))
