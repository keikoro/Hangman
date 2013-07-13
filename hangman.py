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
# - differentiate between plural & singular form for tries left (5 tries vs. 1 try)
# - adjust *displayed* countdown of incorrect guesses (currently counts down from 9 to 0/-1)
# - rearrange print statements (reduce lines)
# - output everything with say (= sound)
# - add more comments!
#
# Ideas for additional/advanced Nice To Have's
# - let user guess the entire word
# - allow phrases and words with hyphens


import random # module for randomisation

def stringtogether(thislist): # function to string together elements in a list
	for element in thislist:
		print(element,end='')
	print()

mywords = ["cherry", "summer", "winter", "programming", "hydrogen", "Saturday",
			"unicorn", "magic", "artichoke", "juice", "hacker", "python", "Neverland",
			"baking", "sherlock", "troll", "batman", "japan", "pastries", "Cairo",
			"Vienna", "raindrop", "waves", "diving", "Malta"]

print("Let's play hangman: guess the word!")
theword = random.choice(mywords)

possibletries = 11 # 11 incorrect guesses are allowed
placeholder = list("-"*len(theword)) # a list consisting of placeholder characters
guessedletters = '' # string for incorrectly guessed letters
mytry = 'tries'

while possibletries > 0:
	stringtogether(placeholder) # create placeholder word

	pickedletter = input("Please pick a letter: ")

	if not pickedletter.isalpha() : # don't allow digits, special characters
		print("Sorry, but {} is not a letter! Try again.".format(pickedletter))

	elif pickedletter in guessedletters: # no multiple guesses of same letter
		print("You already guessed the letter {}!".format(pickedletter))

	else:

		pickedletter = pickedletter.lower() # lowercase all input

		if pickedletter in theword.lower():
			print("You guessed correctly - well done!")
			
			# replace placeholder letters with correctly guessed ones
			letterposition = 0
			for letterexists in theword.lower():
				if letterexists == pickedletter:
					placeholder[letterposition] = theword[letterposition]
				letterposition += 1

		else:
			# add incorrect letters to guessedletters
			guessedletters += pickedletter			
			possibletries -= 1
			print("Sorry, that guess was wrong! Try again.")

		if (guessedletters != '') and (possibletries > 0):
			if possibletries == 1:
				mytry = 'try' 

			print("Incorrectly guessed letters so far: " +guessedletters+ ".\nYou have {} {} left".format(possibletries,mytry))

		if not "-" in placeholder:
			print("We have a winner! Thanks for playing.")
			break

else:
	print("Game over. :( ")

print("The word we you were looking for was: " +theword+ ".")
