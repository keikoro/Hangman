# -*- coding: utf-8 -*-
# Make Hangman playable on different devices
# with Kivy http://kivy.org/

from __future__ import print_function # for python2.x
import random
import glob
import sys # module for parameters
import kivy
kivy.require('1.7.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import *
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.clock import Clock

# only in version 1.8.0
# from kivy.uix.behaviors import ButtonBehavior
# from kivy.uix.behaviors import *
# class ImageButton(ButtonBehavior, Image):
#     pass

def callback_pos(instance, value):
    """Give back the value of a certain position."""
    print('The widget', instance, 'moved to', value)
    return value

def print_it(instance, value):
    """Print Hangman based on position of Hangman grid."""

    # currently prints randomly coloured squares :P
    print(value)

    a = random.random()
    b = random.random()
    c = random.random()

    myvalue = 300 * random.random()

    with instance.canvas:
        # clear()
        Color(a, b, c)
        Rectangle(pos=(myvalue, myvalue), size=(myvalue/2, myvalue/2))

def createMyWords(language, validletters='abcdefghijklmnopqrstuvwxyz',
 additionals=''):
    """Return a list of guessable words.

    Ideally, these words originate from an included dictionary file
    called de-en.dict.
    """
    mywords = set()     # guessable words
    if language == 'en':
        languagepick = 2
    else:
        languagepick = 0
    try:
        myfile = open("de-en.dict")
        for line in myfile:
            # EN = 2, DE = 0
            mywordsplit = line.partition(':: ')[languagepick]
            myword = mywordsplit.partition(' ')[0]
            if len(myword) < 5:     # filter out certain words
                pass
            elif not (myword.lower()).isalpha():
                pass
            else:
                for letter in myword.lower():
                    if (letter not in validletters) and (
                        letter not in additionals):
                        break
                else:
                    mywords.add(myword)
        myfile.close()
    except:     # fallback list of words if dict file isn't found
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
        return mywords

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
    return list(occurencestring.lower())

class HangmanApp(App):
    """Main app."""
    def build(self):
        return MainGrid()

class MainGrid(GridLayout):
    """1st level grid. The main grid of the app.

    This is where ALL the labels, buttons, inputs etc. go."""
    def __init__(self, **kwargs):
        super(MainGrid, self).__init__(**kwargs)
        self.voice = False
        self.wordlanguage = 'en'
        self.cols = 1
        self.possibletries = 11     # 11 incorrect guesses allowed
        self.randomword = ''
        self.myword = ''
        self.placeholderchar = '_ '
        self.placeholdercharvoiced = 'blank'
        self.tryword = 'tries'
        self.incorrectguesses = []   # string for incorrectly guessed letters
        self.correctguesses = ''

        # extended alphabet chars (cannot be used in Python 2!)
        if sys.version_info[0] < 3:
            self.extendedalpha = ''
        else:
            self.extendedalpha = {"ä":"ae", "ö":"oe", "ü":"ue", "ß":"ss",
                "é":"e", "è":"e"}

        # start actual game
        self.randomword, self.theword = self.pickAWord(
            self.wordlanguage, self.extendedalpha)

        self.occurencelist = analyseWords(self.mywords, additionals='')
        self.placeholderword = list(self.placeholderchar*len(self.theword))
        self.placeholderword_str = ''.join(self.placeholderword)

        # title widget
        self.title = TitleBlock()
        self.add_widget(self.title)

        # placeholder word
        self.guessword = PlaceholderWordBlock()
        self.add_widget(self.guessword)
        self.guessword.blankword.text = self.placeholderword_str

        self.alabel = Label(text="empty labellll")
        self.add_widget(self.alabel)

        # hangman goes here
        self.userinput = InputBlock()
        self.add_widget(self.userinput)
        self.userinput.height = 20

        self.message = MessageBlock()
        self.add_widget(self.message)

        # settings and exit button
        self.settingsexit = SettingsExitBlock()
        self.add_widget(self.settingsexit)

        # just checking for correct output
        # TODO remove at end
        print("The word to guess is: ", self.theword)

    def settings_popup(self):
        description = Label(text='Here you can change the settings\n'
            'of the game', height='100sp')
        voiceon = ToggleButton(group="voice", state="down",
            text='text-to-speech', size_hint_y=None, height='50sp')
        voiceoff = ToggleButton(group="voice", text='text-only',
            size_hint_y=None, height='50sp')
        lang_en = ToggleButton(group="language", state="down",
            text='English words', size_hint_y=None, height='50sp')
        lang_de = ToggleButton(group="language", text='German words',
            size_hint_y=None, height='50sp')
        closebutton = Button(text='Apply settings',
            size_hint_y=None, height='50sp')

        content = BoxLayout(orientation='vertical')
        # content = GridLayout(cols=2)
        # TODO turn this into a two-column layout

        content.add_widget(description)
        content.add_widget(voiceon)
        content.add_widget(voiceoff)
        content.add_widget(lang_en)
        content.add_widget(lang_de)
        content.add_widget(closebutton)

        self.popup = Popup(content=content, title='Hangman settings',
                      size_hint=(None, None), size=('300dp', '400dp'))

        closebutton.bind(on_release=self.close_popup)
        voiceon.bind(on_release=self.turn_voice_on)
        voiceoff.bind(on_release=self.turn_voice_off)
        lang_en.bind(on_release=self.pick_lang_en)
        lang_de.bind(on_release=self.pick_lang_de)

        self.popup.open()
        col = AnchorLayout()
        return col

    def pick_lang_en(self, bla):
        self.wordlanguage = 'en'
        print("language: ", self.wordlanguage)

    def pick_lang_de(self, bla):
        self.wordlanguage = 'de'
        print("language: ", self.wordlanguage)

    def turn_voice_on(self, bla):
        self.voice = True
        print("voice: ", self.voice)

    def turn_voice_off(self, bla):
        self.voice = False
        print("voice: ", self.voice)

    def pickAWord(self, wordlanguage, additionals):
        theword = []
        self.mywords = createMyWords(wordlanguage, additionals='')
        randomword = random.choice(list(self.mywords))
        for letter in randomword.lower():
            if self.extendedalpha and (letter in self.extendedalpha):
                letter = self.extendedalpha[letter]
            theword.append(letter)
        theword = ''.join(theword)
        return randomword, theword

    def close_popup(self, bla):
        self.randomword, self.theword = self.pickAWord(self.wordlanguage,
            additionals='')
        self.placeholderword = list(self.placeholderchar*len(self.theword))
        self.placeholderword_str = ''.join(self.placeholderword)

        self.word_to_guess.text = self.placeholderword_str

        self.popup.dismiss()

        print("word language is: ", self.wordlanguage)
        print("this is the word: ", self.theword)
        print(self.placeholderword)

class TitleBlock(GridLayout):
    """2nd level grid for Hangman graphic and user input."""
    def __init__(self, **kwargs):
        super(TitleBlock, self).__init__(**kwargs)
        self.cols = 1

        self.title = Label(text='Let\'s play Hangman!\nGuess the word:')
        self.add_widget(self.title)

class PlaceholderWordBlock(GridLayout):
    """2nd level grid for Hangman graphic and user input."""
    def __init__(self, **kwargs):
        super(PlaceholderWordBlock, self).__init__(**kwargs)
        self.cols = 2
        self.row_default_height=300

        self.graphicsblock = HangmanBlock()
        self.add_widget(self.graphicsblock)

        # the word to be guessed
        self.blankword = Label(text="")
        self.add_widget(self.blankword)


class InputBlock(GridLayout):
    """2nd level grid for Hangman graphic and user input."""
    def __init__(self, **kwargs):
        super(InputBlock, self).__init__(**kwargs)
        self.cols = 2

        self.tries = Label(text="11 tries left")
        self.add_widget(self.tries)

        self.userinput = UserInput()
        self.add_widget(self.userinput)


class HangmanBlock(GridLayout):
    """3rd level grid for Hangman graphic."""
    def __init__(self, **kwargs):
        super(HangmanBlock, self).__init__(**kwargs)
        self.rows = 2
        # self.row_force_default=True
        # self.row_default_height=180
        self.imgsource = 'images/hangman-1-dead.png'
        self.imageliste = glob.glob('images/*.png')

        self.hangmanpic = Image(source=self.imgsource, size=(600,600))
        self.add_widget(self.hangmanpic)

        self.displaywrongletters = Label(text='wrong letters go here')
        self.add_widget(self.displaywrongletters)

        self.bind(pos=callback_pos)

class HangmanGraphics(GridLayout):
    """3rd level grid for Hangman graphic."""
    def __init__(self, **kwargs):
        super(HangmanGraphics, self).__init__(**kwargs)
        self.rows = 2
        self.row_force_default=True
        self.row_default_height=180
        self.imgsource = 'images/hangman-1-dead.png'

        self.hangmanpic = Image(source=self.imgsource, size=(600,600))
        self.add_widget(self.hangmanpic)

        self.displaywrongletters = Label(text='wrong letters go here')
        self.add_widget(self.displaywrongletters)

        self.bind(pos=callback_pos)

class UserInput(GridLayout):
    """3rd level grid for user text input and confirmation button.

    Input field for the letter the user wants to guess and a button to
    confirm the input."""
    def __init__(self, **kwargs):
        super(UserInput, self).__init__(**kwargs)
        self.rows = 2

        self.userinput = TextInput(text='', multiline=False, focus=True)
        self.add_widget(self.userinput)
        self.userinput.bind(text=self.onLetterInput)

        self.onLetterConfirm = Button(text="OK", font_size=14)
        self.add_widget(self.onLetterConfirm)
        self.onLetterConfirm.bind(on_press=self.defocus)
        self.onLetterConfirm.bind(on_press=self.startGuessing)

    def onLetterInput(self, instance, value):
        # print("the letter is: ", content)
        self.theinput = value.lower().encode("utf-8")
        return self.theinput

    def defocus(self, instance):
        """Take focus away from textinput field."""
        self.userinput.focus = False

    def startGuessing(self, instance):
        """Start actual program when user starts guessing letters."""

        # main loop
        self.possibletries = self.parent.parent.possibletries

        if self.theinput and self.possibletries > 0:
            print("possibletries: ", self.possibletries) # TODO remove laterz
            print("the word is: ", self.parent.parent.theword) # TODO remove laterz
            self.parent.parent.triesleft.emptylabel.text = self.parent.parent.theword # TODO remove laterz

            self.pickedletter = self.theinput
            self.userinput.text = ''

            if self.pickedletter and self.pickedletter.isalpha():
                if len(self.pickedletter) > 0:
                        self.pickedletter = self.pickedletter[0]

                print("pickedletter: ", self.pickedletter)
                print("incorrect guesses: ", self.parent.parent.incorrectguesses)

                if self.pickedletter in self.parent.parent.incorrectguesses:
                    print("already in incorrect guesses!")
                else:
                    print("not yet in incorrect guesses!")

                if self.pickedletter in self.parent.parent.theword:
                    print("correct guess")
                else:
                    print("incorrect guess :(")
                    self.parent.parent.incorrectguesses.append(self.pickedletter)
                    print("incorrect guesses: ", self.parent.parent.incorrectguesses)
            else:
                self.parent.parent.triesleft.emptylabel.text = "Sorry, but {} isn't a valid guess! Try again.".format(self.pickedletter)

    # # main loop
    # while possibletries > 0:
    #     output("Please pick a letter: ", blankchar=placeholderchar,
    #         blankcharvoiced=placeholdercharvoiced, software=voicesoftware,
    #         voice=sound, ending='')
    #     # lowercasing picked letter
    #     # for easier handling of extended characters (ä, ß etc.)
    #     pickedletter = flexibleInput().lower()

    #     if pickedletter == '???':
    #         occurencestringpretty = ''
    #         for char in str(occurencelist):
    #             if char not in "'[]":
    #                 occurencestringpretty += char
    #         output("Clever you! The most common letters are: {}"
    #             .format(occurencestringpretty.upper()),
    #             blankchar=placeholderchar,
    #             blankcharvoiced=placeholdercharvoiced,
    #             software=voicesoftware, voice=sound)
    #         continue

    #     if len(pickedletter) > 0:
    #         # match full word if word length matches
    #         if len(pickedletter) == len(theword):
    #             fullguesses -= 1
    #             if fullguesses == 1:
    #                 timesword = 'time'
    #             if fullguesses >= 0:
    #                 if pickedletter == theword.lower():
    #                     placeholderword = theword.lower()
    #                     output("\nYour guess was spot on!",
    #                         blankchar=placeholderchar,
    #                         blankcharvoiced=placeholdercharvoiced,
    #                         software=voicesoftware, voice=sound,
    #                         ending='')
    #                     pickedword = True
    #                 else:
    #                     if fullguesses > 0:
    #                         output("Sorry, your guess was wrong. "
    #                             "You may guess the full word {} more {}."
    #                             .format(fullguesses, timesword),
    #                             blankchar=placeholderchar,
    #                             blankcharvoiced=placeholdercharvoiced,
    #                             software=voicesoftware, voice=sound)
    #                     else:
    #                         output("\nGame over. :( ",
    #                             blankchar=placeholderchar,
    #                             blankcharvoiced=placeholdercharvoiced,
    #                             software=voicesoftware, voice=sound)
    #                         break
    #             else:
    #                 break
    #         else:
    #             pickedletter = pickedletter[0]
    #     if pickedletter == '?':
    #         output("You could try guessing the letter '{}'."
    #             .format(showHint(occurencelist)), blankchar=placeholderchar,
    #             blankcharvoiced=placeholdercharvoiced,
    #             software=voicesoftware, voice=sound)
    #         continue
    #     if extendedalpha and (pickedletter in extendedalpha):
    #         if pickedletter not in extendedalphaspecial:
    #             output("Sorry, but '{}' isn't a valid guess! Try again."
    #                 .format(pickedletter.upper()), blankchar=placeholderchar,
    #                 blankcharvoiced=placeholdercharvoiced,
    #                 software=voicesoftware, voice=sound)
    #         else:
    #             output("Sorry, but '{}' isn't a valid guess! Try again."
    #                 .format(pickedletter), blankchar=placeholderchar,
    #                 blankcharvoiced=placeholdercharvoiced,
    #                 software=voicesoftware, voice=sound)
    #         continue
    #     if not pickedletter.isalpha():  # disallow digits, special chars
    #         output("Sorry, but you didn't type a letter! Try again."
    #             .format(pickedletter), blankchar=placeholderchar,
    #             blankcharvoiced=placeholdercharvoiced,
    #             software=voicesoftware, voice=sound)
    #         continue
    #     if pickedletter in incorrectguesses:    # letter was already guessed
    #         output("You already guessed the letter '{}'!"
    #             .format(pickedletter.upper()), blankchar=placeholderchar,
    #             blankcharvoiced=placeholdercharvoiced,
    #             software=voicesoftware, voice=sound)
    #         continue
    #     if pickedletter in correctguesses:
    #         output("You already successfully picked '{}'!"
    #             .format(pickedletter.upper()), blankchar=placeholderchar,
    #             blankcharvoiced=placeholdercharvoiced,
    #             software=voicesoftware, voice=sound)
    #         continue

    #     # correct guess
    #     if pickedletter in theword.lower() and pickedword is not True:
    #         letterposition = 0
    #         for letterexists in theword.lower():
    #             if letterexists == pickedletter:
    #                 placeholderword[letterposition] = (
    #                     theword.upper()[letterposition])
    #             letterposition += 1
    #         output("You guessed correctly, well done!",
    #             blankchar=placeholderchar,
    #             blankcharvoiced=placeholdercharvoiced,
    #             software=voicesoftware,
    #             voice=sound)
    #         correctguesses += pickedletter
    #     # incorrect guess
    #     elif len(pickedletter) == 1:
    #         incorrectguesses += pickedletter
    #         possibletries -= 1
    #         output("Sorry, '{}' is an incorrect guess!"
    #             .format(pickedletter.upper()), blankchar=placeholderchar,
    #             blankcharvoiced=placeholdercharvoiced,
    #             software=voicesoftware, voice=sound)

    #         print(hangman(possibletries))   # print hangman

    #         if (incorrectguesses != '') and (possibletries > 0):
    #             if possibletries == 1:
    #                 tryword = 'try'
    #             output(incorrectguesses.upper(), ending='\n\n', spell=False,
    #                 blankchar=placeholderchar,
    #                 blankcharvoiced=placeholdercharvoiced,
    #                 software=voicesoftware, voice=False)
    #             output("Incorrectly guessed letters so far: ",
    #                 blankchar=placeholderchar,
    #                 blankcharvoiced=placeholdercharvoiced,
    #                 software=voicesoftware, spell=False,
    #                 voice=sound, ending='', outputtext=False)
    #             output(incorrectguesses.upper(), ending='', spell=True,
    #                 blankchar=placeholderchar,
    #                 blankcharvoiced=placeholdercharvoiced,
    #                 software=voicesoftware,
    #                 voice=sound, outputtext=False)
    #             output("You have {} {} left."
    #                 .format(possibletries,tryword),
    #                 blankchar=placeholderchar,
    #                 blankcharvoiced=placeholdercharvoiced,
    #                 software=voicesoftware, voice=sound)
    #     # ----- end guessing

    #     # remove pickedletter from hint list
    #     if pickedletter in occurencelist:
    #         occurencelist.remove(pickedletter)
    #     if not placeholderchar in placeholderword:
    #         # if pickedword is not True:
    #         #     output("\n")
    #         output("\nWe have a winner! Thanks for playing. :)",
    #             blankchar=placeholderchar,
    #             blankcharvoiced=placeholdercharvoiced,
    #             software=voicesoftware, voice=sound)
    #         break
    #     if placeholderword == list(placeholderchar*len(theword)):
    #         output(stringtogether(placeholderword),
    #             blankchar=placeholderchar,
    #             blankcharvoiced=placeholdercharvoiced,
    #             software=voicesoftware, voice=False)    # show whole blank word
    #         if sound:
    #             try:
    #                 output("The word you're looking for has {} letters"
    #                     .format(len(theword)), software=voicesoftware,
    #                     outputtext=False)
    #             except:
    #                 print(t2s_errormsg)
    #     if possibletries > 0 and placeholderword != list(placeholderchar*len(theword)):
    #         output("The word is: ", ending='', blankchar=placeholderchar,
    #             blankcharvoiced=placeholdercharvoiced,
    #             software=voicesoftware, voice=sound)
    #         output(stringtogether(placeholderword), spell=True,
    #             blankchar=placeholderchar,
    #             blankcharvoiced=placeholdercharvoiced,
    #             software=voicesoftware,
    #             voice=sound)
    # else:
    #     output("\nGame over. :( ", blankchar=placeholderchar,
    #         blankcharvoiced=placeholdercharvoiced,
    #         software=voicesoftware, voice=sound)
    # output("The word you were looking for was: {}.".format(randomword),
    #     blankchar=placeholderchar, blankcharvoiced=placeholdercharvoiced,
    #     software=voicesoftware, voice=sound)


        #         # this print works
        #         print("this is the picked letter: ", self.pickedletter) # prints out current value of input field

        #         # letter was already guessed
        #         if self.pickedletter in self.parent.parent.incorrectguesses:
        #             self.parent.parent.triesleft.emptylabel.text = "bla"

        #             print("You already guessed the "
        #                 "letter '{}'!".format(self.pickedletter.upper()))

        #         self.parent.parent.word_to_guess.text = ''.join(
        #             self.parent.parent.placeholderword)
        #         self.parent.graphicsblock.wrongletters.text += self.pickedletter
        #         self.userinput.text = ''

        #         print(self.parent.parent.theword.lower())

        #         if self.pickedletter not in self.parent.parent.theword.lower():
        #             # this doesn't work! always prints when it shouldn't always!
        #             print("letter exists!")
        #             letterposition = 0
        #             for letterexists in self.parent.parent.theword.lower():
        #                 if letterexists == self.pickedletter:
        #                     self.parent.parent.placeholderword[letterposition] = (
        #                         self.parent.parent.theword.upper()[letterposition])
        #                 letterposition += 1
        #             self.parent.parent.correctguesses += self.pickedletter
        #             print(self.parent.parent.correctguesses)
        #         else:
        #             print(self.pickedletter, " is wrong")
        #             self.parent.parent.incorrectguesses.append(self.pickedletter)
        #             print("incorrect guesses are: ", self.parent.parent.incorrectguesses)


        #         self.parent.parent.possibletries -= 1

        #         if self.parent.parent.possibletries == 1:
        #             self.parent.parent.tryword = 'try'

        #         if self.parent.parent.possibletries > 0:
        #             thistext = "{} {} left".format(
        #                 self.parent.parent.possibletries,
        #             self.parent.parent.tryword)
        #         else:
        #             thistext = "Game over. :( "

        #         self.parent.graphicsblock.hangman.source = self.parent.imageliste[
        #             self.parent.parent.possibletries]
        #         self.parent.parent.triesleft.tries.text = thistext

        # wrong letters

class MessageBlock(GridLayout):
    """Shows how many tries are left."""
    def __init__(self, **kwargs):
        super(MessageBlock, self).__init__(**kwargs)
        self.cols = 1

        self.emptylabel = Label(text='This is the message block')
        self.add_widget(self.emptylabel)

class SettingsExitBlock(GridLayout):
    """2nd level grid for row with Info button and Exit button."""
    def __init__(self, **kwargs):
        super(SettingsExitBlock, self).__init__(**kwargs)
        self.cols = 2
        self.row_default_height=50

        self.settingsbutton = Button(text='Settings', font_size=14)
        self.add_widget(self.settingsbutton)
        self.settingsbutton.bind(on_press=self.callback)

        self.exitbutton = Button(text='Exit game', font_size=14)
        self.add_widget(self.exitbutton)
        self.exitbutton.bind(on_press=self.debug)

    def callback(self, value):
        print("this is the info button")
        self.parent.settings_popup()

    def debug(self, value):
        print("debug msg... voice: ", self.parent.voice,", language: ",
            self.parent.wordlanguage)

if __name__ == '__main__':
    m = HangmanApp().run()
