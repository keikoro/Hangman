#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# A Hangman game programmed in Python 3.
#
# Copyright (c) 2013 K Kollmann <code∆k.kollmann·moe>
# License: http://opensource.org/licenses/MIT MIT
#
# You need to have Python 3.x installed to run this game.
# The game's objective is to guess a word, letter by letter.
# 11 incorrect guesses are possible, then hangman dies and the game is over.
#
# Parameters the game can be run with:
# -nosound to turn off text-to-speech
# -en|de to play with English or German words # TODO: (defaults to English)
#
"""Hangman - a word-guessing game.

parameters:
-nosound ... play the game without sound
-en|de ... play the game with English/German words
"""

from __future__ import print_function # for python2.x
import random # module for randomisation
import subprocess # enable command line functions
import sys # module for parameters

def hangman(leftovertries):
    """Print out hangman ASCII graphic on incorrect guesses."""
    allhangmans = [
"""  ______
  |/   |
  |    o
  |   ´|`
  |   / \\
__|________""",
"""  ______
  |/   |
  |    o
  |   ´|`
  |   /
__|________""",
"""  ______
  |/   |
  |    o
  |   ´|`
  |
__|________""",
"""  ______
  |/   |
  |    o
  |   ´|
  |
__|________""",
"""  ______
  |/   |
  |    o
  |    |
  |
__|________""",
"""  ______
  |/   |
  |    o
  |
  |
__|________""",
"""  ______
  |/   |
  |
  |
  |
__|________""",
"""  ______
  |/
  |
  |
  |
__|________""",
"""  ______
  |
  |
  |
  |
__|________""",
"""
  |
  |
  |
  |
__|________""",
"""




___________""",
    ]
    return allhangmans[leftovertries]

def stringtogether(alist):
    """return elements in a list as a string"""
    return ''.join(alist)

def output(text, blankchar='-', blankcharvoiced='blank', software='say',
    voice=True, outputtext=True, ending='\n', spell=False):
    """Print out text and voice it using text-to-speech software.

    If outputtext is True, print text.
    If voice is True, voice text with text-to-speech.
    """
    maxvoicedblanks = 2
    t2s_errormsg = ("There was a problem with running the text-to-speech "
        "software {}.".format(software))
    # spell out placeholder characters explicitely
    if text and outputtext == True:
        print(text,end=ending)
    if voice:
        if spell:
            # don't spell out all placeholder chars
            speaklist = []
            howmanyblanks = 0
            for char in text:
                if char == blankchar:
                    howmanyblanks += 1
                else:
                    if howmanyblanks > 0:
                        # append no. of blank characters
                        if howmanyblanks > maxvoicedblanks:
                            speaklist.append("{} {}s ".format(howmanyblanks,
                                blankcharvoiced))
                        else:
                            for x in range(howmanyblanks):
                                speaklist.append(blankcharvoiced)
                    speaklist.append(char)
                    howmanyblanks = 0

            if char == blankchar: # needed for when last character is a dot
                if howmanyblanks > maxvoicedblanks:
                    speaklist.append("{} {}s ".format(howmanyblanks,
                        blankcharvoiced))
                else:
                    for x in range(howmanyblanks):
                        speaklist.append(blankcharvoiced)

            for element in speaklist:
                try:
                    subprocess.call([software, element])
                except:
                    print(t2s_errormsg)
        else:
            try:
                subprocess.call([software, text])
            except:
                print(t2s_errormsg)

def analyseWords(mywords, additionals=''):
    """Analyse mywords and return all used characters.

     The characters are sorted by occurence (descending).
     """
    mydict = {}
    moreletters = []
    for word in mywords: # create dict with occurence of letters in all words
        for letter in word.lower():
            if additionals and (letter in additionals):
                moreletters = additionals[letter]
                for letter in moreletters:
                    if letter in mydict:
                        mydict[letter] += 1
                    else:
                        mydict[letter] = 1
            if letter in mydict:
                mydict[letter] += 1
            else:
                mydict[letter] = 1

    # pairs in mydict dictionary sorted by occurence (descending)
    # http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value
    # pairlist looks like this: [('e', 167410), ('n', 100164),...]
    pairlist = sorted(mydict.items(), key=lambda x: x[1], reverse=True)
    occurencestring = ''
    for pair in pairlist:
        occurencestring += pair[0] # use 1st element of each pair
    return list(occurencestring.upper())

def showHint(occurencelist):
    """Returns the first element of occurencelist as string."""
    return str(occurencelist[0])

def checkOS():
    """Determine OS and choose corresponding text-to-speech software."""
    if sys.platform == 'darwin':
        return 'say'
    elif (sys.platform == 'linux') or (sys.platform == 'win32'):
        return 'espeak'
    else:
        return 'espeak'

def createMyWords(language, validletters, additionals=''):
    """Return a list of guessable words.

    Ideally, these words originate from a dictionary file
    called de-en.dict.
    """
    mywords = set() # guessable words
    if language == 'en':
        languagepick = 2
    else:
        languagepick = 0
    try: # filter out 5+ letter words from dict file
        myfile = open("de-en.dict")
        for line in myfile:
            # OLD myword = line.split()[0]
            mywordsplit = line.partition(':: ')[languagepick] # EN = 2, DE = 0
            myword = mywordsplit.partition(' ')[0]
            for letter in myword.lower():
                if len(myword) < 5:
                    break
                if not letter in validletters:
                    if additionals and (letter in additionals):
                        mywords.add(myword)
                    else:
                        break
            else:
                mywords.add(myword)
        myfile.close()
    except: # fallback list of words if dict file isn't found
        if language == 'en': # EN list
            mywords = {"cherry", "summer", "winter", "programming", "hydrogen",
                "Saturday", "unicorn", "magic", "artichoke", "juice",
                "hacker", "python", "Neverland", "baking", "sherlock",
                "troll", "batman", "japan", "pastries", "Cairo", "Vienna",
                "raindrop", "waves", "diving", "Malta", "cupcake", "ukulele"}
        else: # DE list
            mywords = {"Ferien", "Grashuepfer", "programmieren", "Polizei",
                "Zielgerade", "Kronkorken", "Kuchen", "rumlungern", "kichern",
                "Salzwasser", "Schwimmflossen", "Motorradhelm", "feiern",
                "Fehlbesetzung", "Regisseurin", "Zuckerwatte", "pieksen",
                "Nebelmaschine", "Lampenschirm", "Redewendung"}
    finally:
        # mywords = ["unicorn"] # use only one word to try out things
        # mywords = ["Hülsenfrüchte"] # use only one word to try out things
        mywords = ["Überbrückungstür"] # use only one word to try out things
        return mywords

def soundcheck(voicesoftware):
    """Check if text-to-speech is possible."""
    print("Starting soundcheck...")
    # test existence of text-to-speech software
    try:
        output("If you can hear a voice and want to play the game with "
            "text-to-speech output, please type yes and press enter. "
            "Otherwise type no and press enter.", software=voicesoftware,
            outputtext=False)
    except:
        print("Please install the programm '{}' to use text-to-speech "
            "(or have your system administrator install it for you)."
            .format(voicesoftware))
        print("Note that you can still play the text-only version of "
            "Hangman even if you don't have '{}' installed!"
            .format(voicesoftware))
        sound = False
    else:
        print("You have the necessary software installed to play Hangman "
            "with text-to-speech output.".format(voicesoftware))
        print("Could you hear your computer talk and do you want to play "
            "with text-to-speech enabled?")
        answer = input("Please type yes or no (and press enter): ")
        # TODO use raw_input() for py2
        # answer = raw_input("Please type yes or no (and press enter): ")
        if len(answer) > 0 and answer.lower()[0] == 'y':
            sound = True
        else:
            sound = False
    finally:
        print("Soundcheck completed, you're ready to play.")
        return sound

def playGame(sound, wordlanguage):
    """the actual Hangman game"""

    # ---- start program
    possibletries = 11 # 11 incorrect guesses allowed
    incorrectguesses = '' # string for incorrectly guessed letters
    correctguesses = ''
    tryword = 'tries'
    timesword = 'times'
    placeholderchar = '-'
    placeholdercharvoiced = 'blank'
    fullguesses = 3
    alphabet = "abcdefghijklmnopqrstuvwxyz" # standard alphabet
    # extended alphabet chars
    extendedalpha = {"ä":"ae", "ö":"oe", "ü":"ue", "ß":"ss", "é":"e", "è":"e"}
    theword = []

    voicesoftware = checkOS()
    t2s_errormsg = ("There was a problem with running the text-to-speech "
        "software {}.".format(voicesoftware))

    if wordlanguage == '':
        wordlanguage = 'en'

    mywords = createMyWords('de', alphabet, additionals=extendedalpha)

    randomword = random.choice(list(mywords))
    for letter in randomword.lower():
        if extendedalpha and (letter in extendedalpha):
            letter = extendedalpha[letter]
        theword.append(letter)
    theword = stringtogether(theword)

    # TODO fix special characters suddenly appearing in occurencelist
    # check createmywords function
    occurencelist = analyseWords(mywords, additionals=extendedalpha)
    placeholderword = list(placeholderchar*len(theword))

    if sound:
        sound = soundcheck(voicesoftware)

    # introduction
    output("Let's play Hangman! You have to guess the word.",
        blankchar=placeholderchar, blankcharvoiced=placeholdercharvoiced,
        software=voicesoftware, voice=sound)
    output("Whenever you want the computer to help you, type in a {}."
        .format("question mark"), blankchar=placeholderchar,
        blankcharvoiced=placeholdercharvoiced, software=voicesoftware,
        voice=sound)
    if sound:
        output("The word you're looking for has {} letters"
        .format(len(theword)), software=voicesoftware, outputtext=False)
    output(stringtogether(placeholderword), blankchar=placeholderchar,
        blankcharvoiced=placeholdercharvoiced, software=voicesoftware,
        voice=False) # show blank word

    # main loop
    while possibletries > 0:
        output("Please pick a letter: ", blankchar=placeholderchar,
            blankcharvoiced=placeholdercharvoiced, software=voicesoftware,
            voice=sound, ending='')
        # uppercasing picked letter like in real Hangman
        pickedletter = input().upper()
        # TODO use raw_input().upper() for py2
        # pickedletter = input().upper()

        if pickedletter == '???':
            occurencestringpretty = ''
            for char in str(occurencelist):
                if char not in "'[]":
                    occurencestringpretty += char
            output("Clever you! The most common letters are: {}"
                .format(occurencestringpretty), blankchar=placeholderchar,
                blankcharvoiced=placeholdercharvoiced,
                software=voicesoftware, voice=sound)
            continue

        if len(pickedletter) > 0:
            # # TODO several letters -> guess whole word
            # if len(pickedletter) == len(theword):
            #     fullguesses -= 1
            #     if fullguesses == 1:
            #         timesword = 'time'
            #     if fullguesses > 0:
            #         if pickedletter == theword.upper():
            #             placeholderword = theword.upper()
            #             output("Your guess was spot on!",
            #                 blankchar=placeholderchar,
            #                 blankcharvoiced=placeholdercharvoiced,
            #                 software=voicesoftware, voice=sound)
            #         else:
            #             output("Sorry, your guess was wrong. You may guess the "
            #                 "full word {} more {}."
            #                 .format(fullguesses, timesword),
            #                 blankchar=placeholderchar,
            #                 blankcharvoiced=placeholdercharvoiced,
            #                 software=voicesoftware, voice=sound)
            #     else:
            #         output("\nGame over. :( ", blankchar=placeholderchar,
            #             blankcharvoiced=placeholdercharvoiced,
            #             software=voicesoftware, voice=sound)
            #         break
            # else:
                pickedletter = pickedletter[0]
        if pickedletter == '?':
            output("You could try guessing the letter '{}'."
                .format(showHint(occurencelist)), blankchar=placeholderchar,
                blankcharvoiced=placeholdercharvoiced,
                software=voicesoftware, voice=sound)
            continue
        # TODO picking a letter in the extended characters set
        # should result in a warning that the letter cannot be picked
        #
        # if extendedalpha and pickedletter in extendedalpha:
        #     output("Sorry, but '{}'' isn't a valid guess! Try again."
        #         .format(pickedletter), blankchar=placeholderchar,
        #         blankcharvoiced=placeholdercharvoiced,
        #         software=voicesoftware, voice=sound)
        if not pickedletter.isalpha() : # disallow digits, special chars
            output("Sorry, but you didn't type a letter! Try again."
                .format(pickedletter), blankchar=placeholderchar,
                blankcharvoiced=placeholdercharvoiced,
                software=voicesoftware, voice=sound)
            continue
        if pickedletter in incorrectguesses: # letter was already guessed
            output("You already guessed the letter '{}'!"
                .format(pickedletter), blankchar=placeholderchar,
                blankcharvoiced=placeholdercharvoiced,
                software=voicesoftware, voice=sound)
            continue
        if pickedletter in correctguesses:
            output("You already successfully picked '{}'!"
                .format(pickedletter.upper()), blankchar=placeholderchar,
                blankcharvoiced=placeholdercharvoiced,
                software=voicesoftware, voice=sound)
            continue

        # correct guess
        if pickedletter in theword.upper():
            letterposition = 0
            for letterexists in theword.upper():
                if letterexists == pickedletter:
                    placeholderword[letterposition] = (
                        theword.upper()[letterposition])
                letterposition += 1
            output("You guessed correctly, well done!",
                blankchar=placeholderchar,
                blankcharvoiced=placeholdercharvoiced,
                software=voicesoftware,
                voice=sound)
            correctguesses += pickedletter
        # incorrect guess
        elif len(pickedletter) == 1:
            incorrectguesses += pickedletter
            possibletries -= 1
            output("Sorry, '{}' is an incorrect guess!"
                .format(pickedletter.upper()), blankchar=placeholderchar,
                blankcharvoiced=placeholdercharvoiced,
                software=voicesoftware, voice=sound)

            print(hangman(possibletries)) # print hangman

            if (incorrectguesses != '') and (possibletries > 0):
                if possibletries == 1:
                    tryword = 'try'
                output(incorrectguesses, ending='\n\n', spell=False,
                    blankchar=placeholderchar,
                    blankcharvoiced=placeholdercharvoiced,
                    software=voicesoftware, voice=False)
                output("Incorrectly guessed letters so far: ",
                    blankchar=placeholderchar,
                    blankcharvoiced=placeholdercharvoiced,
                    software=voicesoftware, spell=False,
                    voice=sound, ending='', outputtext=False)
                output(incorrectguesses, ending='', spell=True,
                    blankchar=placeholderchar,
                    blankcharvoiced=placeholdercharvoiced,
                    software=voicesoftware,
                    voice=sound, outputtext=False)
                output("You have {} {} left."
                    .format(possibletries,tryword),
                    blankchar=placeholderchar,
                    blankcharvoiced=placeholdercharvoiced,
                    software=voicesoftware, voice=sound)
        # ----- end guessing

        # remove pickedletter from hint list
        if pickedletter in occurencelist:
            occurencelist.remove(pickedletter)
        if not placeholderchar in placeholderword:
            output("We have a winner! Thanks for playing. :)",
                blankchar=placeholderchar,
                blankcharvoiced=placeholdercharvoiced,
                software=voicesoftware, voice=sound)
            break
        if placeholderword == list(placeholderchar*len(theword)):
            output(stringtogether(placeholderword),
                blankchar=placeholderchar,
                blankcharvoiced=placeholdercharvoiced,
                software=voicesoftware, voice=False) # show whole blank word
            if sound:
                try:
                    output("The word you're looking for has {} letters"
                        .format(len(theword)), software=voicesoftware,
                        outputtext=False)
                except:
                    print(t2s_errormsg)
        else:
            output("The word is: ", ending='', blankchar=placeholderchar,
                blankcharvoiced=placeholdercharvoiced,
                software=voicesoftware, voice=sound)
            output(stringtogether(placeholderword), spell=True,
                blankchar=placeholderchar,
                blankcharvoiced=placeholdercharvoiced,
                software=voicesoftware,
                voice=sound)
    else:
        output("\nGame over. :( ", blankchar=placeholderchar,
            blankcharvoiced=placeholdercharvoiced,
            software=voicesoftware, voice=sound)
    output("The word you were looking for was: " +randomword+ '.',
        blankchar=placeholderchar, blankcharvoiced=placeholdercharvoiced,
        software=voicesoftware, voice=sound)

# ------- variables not part of functions -------
sound = True
wordlanguage = ''
voicesoftware = ''

# call playGame() function when file is opened
if __name__ == "__main__":
    if len(sys.argv) > 1:   # check for parameter input
        # begin loop
        argumentlist = sys.argv[1:]    # all args but filename (= 1st arg)
        for argument in argumentlist:
            thisargument = argument.lower()
            if (thisargument == "-nosound") or (thisargument == "nosound"):
                sound = False
                continue
            if ((thisargument == "en") or (thisargument == "-en") or
             (thisargument == "de") or (thisargument == "-de")):
                if "en" in thisargument:
                    if wordlanguage != '':
                        print("You entered more than one parameter for "
                            "language - Hangman will now default to English.")
                    wordlanguage = "en"
                else:
                    if wordlanguage != '':
                        print("You entered more than one parameter for "
                            "language - Hangman will now default to German.")
                    wordlanguage = "de"
    playGame(sound, wordlanguage)
