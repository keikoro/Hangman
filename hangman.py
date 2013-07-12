# A simple hangman game in Python

# Additional features
#
# DONE
# - warning if there's non-letter input
# - warning if letter was already previously guessed
# - only list incorrect letters in separate list (correct ones are displayed anyway)
# - letter matching should ignore upper/lowercase
#
# TODO
# 
# - get words-to-be-guessed from a file
# - hangman (graphics)


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
