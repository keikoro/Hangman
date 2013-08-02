# -*- coding: utf-8 -*-
# Make Hangman playable on different devices
# with Kivy http://kivy.org/

from __future__ import print_function # for python2.x
import random
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

# only in version 1.8.0
# from kivy.uix.behaviors import *

# only in version 1.8.0
# class ImageButton(ButtonBehavior, Image):
#     pass


def callback_pos(instance, value):
    """Give back the value of a certain position."""
    print('The widget', instance, 'moved to', value)
    return value

# def callback(instance):
#     print('The button {} is being pressed'.format(instance.text))

def on_enter(instance, value):
    print('User pressed enter in', instance, ' and typed ', value)

# def on_text(instance, value):
#     print('The widget', instance, 'have:', value)

def change_img(instance, value):
    """Change image on image click."""

    print(value)
    print("Bild wurde geklickt")

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
        # mywords = ["unicorn"] # use only one word to try out things
        # mywords = ["Hülsenfrüchte"] # use only one word to try out things
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
        # return Label(text='Hello world')
        return MainGrid()

class MiniGrid(GridLayout): # only needed as 'template' right now
    def __init__(self, **kwargs):
        super(MiniGrid, self).__init__(**kwargs)
        self.cols = 2
        self.buttoninfo = Button(text='Info', font_size=14)
        self.add_widget(self.buttoninfo)
        #self.add_widget(Label(text='6. Zeile, 2. Spalte'))
        self.buttonexit = Button(text='Exit game', font_size=14)
        self.add_widget(self.buttonexit)

class GridHangmanRow(GridLayout):
    """2nd level grid for Hangman graphic and user input."""
    def __init__(self, **kwargs):
        super(GridHangmanRow, self).__init__(**kwargs)
        self.cols = 2

        # self.img1 = 'logo-kivy.png'
        # self.img2 = 'green.png'

        self.imageliste = ['logo-kivy.png', 'green.png']

        self.drawblock = GridHangman()
        self.add_widget(self.drawblock)

        self.guessblock = GridUserInput()
        self.add_widget(self.guessblock)

        # self.wrongletterswidget = GridUserInput()
        # self.add_widget(self.wrongletterswidget)

class GridHangman(GridLayout):
    """3rd level grid for Hangman graphic."""
    def __init__(self, **kwargs):
        super(GridHangman, self).__init__(**kwargs)
        self.rows = 2
        self.x = 2

        # if self.x%2 == 0:
        #     hangman_img = 'logo-kivy.png'
        # else:
        #     hangman_img = 'green.png'

        self.imgsource = 'logo-kivy.png'

        self.hangman = Image(source=self.imgsource)
        self.add_widget(self.hangman)
        self.hangman.bind(on_press=change_img)

        #self.x += 1
        # buttons.bind(on_press = self.t1.insert_text(str(item)))

        self.wrongletters = Label(text='')
        self.add_widget(self.wrongletters)

        self.bind(pos=callback_pos)

class GridUserInput(GridLayout):
    """3rd level grid for user input and OK button.

    Features and input field for the letter the user wants to guess and a
    button to confirm the input."""
    def __init__(self, **kwargs):
        super(GridUserInput, self).__init__(**kwargs)
        self.rows = 2
        self.userinput = TextInput(text='', multiline=False)
        self.add_widget(self.userinput)
        # self.userinput.bind(on_text_validate=on_enter)
        self.userinput.bind(text=self.on_text)

        self.okbutton = Button(text='OK', font_size=14)
        self.add_widget(self.okbutton)
        self.okbutton.bind(on_press=self.okclick)

    def okclick(self, value):
        print(self.currenttext)


        self.parent.parent.word_to_guess.text = ''.join(
            self.parent.parent.placeholderword)
        self.parent.drawblock.wrongletters.text += self.currenttext
        self.userinput.text = ''

        self.parent.parent.possibletries -= 1
        thistext = "{} tries left".format(self.parent.parent.possibletries)

        self.parent.drawblock.hangman.source = random.choice(self.parent.imageliste)
        self.parent.parent.triesleft.tries.text = thistext

        # wrong letters


    def on_text(self, memaddress, content):
        print('The widget', content, 'have:', memaddress)
        self.currenttext = content

class GridTriesLeft(GridLayout):
    """Shows how many tries are left."""
    def __init__(self, **kwargs):
        super(GridTriesLeft, self).__init__(**kwargs)
        self.cols = 2

        # thistryno = 11
        # thistext = "You have {} tries left.".format(thistryno)

        self.tries = Label(text="11 tries left")
#        self.tries = Label(text="You have {} tries left.".format(self.parent.possibletries))


        self.add_widget(self.tries)
        self.emptylabel = Label(text="")
        self.add_widget(self.emptylabel)


class GridInfoExit(GridLayout):
    """2nd level grid for row with Info button and Exit button."""
    def __init__(self, **kwargs):
        super(GridInfoExit, self).__init__(**kwargs)
        self.cols = 2
        self.infobutton = Button(text='Info', font_size=14)
        self.add_widget(self.infobutton)
        self.infobutton.bind(on_press=self.callback)

        # self.exitwidget = Widget(height=200, width=300)
        # self.exitbutton = Button(text='New exit', font_size=14)
        # self.exitwidget.add_widget(self.exitbutton)

        # with self.exitwidget.canvas:
        #     Color(0.5, 0.7, 0)

        self.exitbutton = Button(text='Exit game', font_size=14)
        self.add_widget(self.exitbutton)
        self.exitbutton.bind(on_release=self.debug)


        # self.infobutton.trigger_action(duration=1)

    def callback(self, value):
        print("this is the info button")
        self.parent.info_popup()
        #print(self.userinput.text)

    def debug(self, value):
        print("voice: ", self.parent.voice, ", language: ",
            self.parent.wordlanguage)
        # super.stop()

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
        # extended alphabet chars (cannot be used in Python 2!)
        if sys.version_info[0] < 3:
            self.extendedalpha = ''
        else:
            self.extendedalpha = {"ä":"ae", "ö":"oe", "ü":"ue", "ß":"ss",
                "é":"e", "è":"e"}
        self.theword = []

        # start actual game
        self.mywords = createMyWords(self.wordlanguage, additionals='')
        self.randomword = random.choice(list(self.mywords))

        self.randomword = random.choice(list(self.mywords))
        for letter in self.randomword.lower():
            if self.extendedalpha and (letter in self.extendedalpha):
                letter = extendedalpha[letter]
            self.theword.append(letter)
        self.theword = ''.join(self.theword)

        self.occurencelist = analyseWords(self.mywords, additionals='')
        self.placeholderword = list(self.placeholderchar*len(self.theword))
        self.placeholderword_str = ''.join(self.placeholderword)


        # title widget
        self.title = Label(text='Blblbllablbl text here')
        self.add_widget(self.title)

        # # subtitle widget
        # self.subtitle = Label(text='Some more [ref=text]info[/ref] on the game...', markup=True)
        # self.subtitle.bind(on_ref_press=print_it)
        # self.add_widget(self.subtitle)

        # the word to be guessed
        self.word_to_guess = Label(text="{}".format(self.placeholderword_str))
        self.add_widget(self.word_to_guess)

        # needs two cols
        #
        self.hangmanrow = GridHangmanRow()
        self.add_widget(self.hangmanrow)

        # # needs 2 cols
        # self.languagerow = GridLangRow()
        # self.add_widget(self.languagerow)

        # needs 2 cols
        self.triesleft = GridTriesLeft()
        self.add_widget(self.triesleft)

        # needs 2 cols
        self.exitrow = GridInfoExit()
        self.add_widget(self.exitrow)

        # open settings popup at beginning of game
        # with delay (otherwise the popup's not overlayed!)
        Clock.schedule_once(self.settings_popup, 1)



    def info_popup(self):
        btnclose = Button(text='Close this popup', size_hint_y=None, height='50sp')
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='This is the info text'))
        content.add_widget(btnclose)
        popup = Popup(content=content, title='This is the popup\'s title',
                      size_hint=(None, None), size=('300dp', '300dp'))
        btnclose.bind(on_release=popup.dismiss)
        button = Button(text='Open popup', size_hint=(None, None),
                        size=('150sp', '70dp'),
                        on_release=popup.open)
        popup.open()
        col = AnchorLayout()
        col.add_widget(button)
        return col

    def settings_popup(self, bla):
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

    def close_popup(self, bla):
        self.popup.dismiss()

        # self.mywords = createMyWords(self.wordlanguage, additionals='')
        # self.randomword = random.choice(list(self.mywords))

        # self.randomword = random.choice(list(self.mywords))
        # for letter in self.randomword.lower():
        #     if self.extendedalpha and (letter in self.extendedalpha):
        #         letter = extendedalpha[letter]
        #     self.theword.append(letter)
        # self.theword = ''.join(self.theword)

        # self.occurencelist = analyseWords(self.mywords, additionals='')
        # self.placeholderword = list(self.placeholderchar*len(self.theword))

        print(self.randomword)
        print(self.placeholderword)


if __name__ == '__main__':
    m = HangmanApp().run()
