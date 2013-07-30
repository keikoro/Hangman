# Make Hangman playable on different devices
# with Kivy http://kivy.org/

import random
import kivy
kivy.require('1.7.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import *
from kivy.uix.image import Image
from kivy.uix.widget import Widget
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

# class ShowImage(Image):
#    pass


class MyApp(App):
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
        # this is a hot mess / in-progress work ;)

        # self.image = ShowImage(source='logo-kivy.png', pos=(200, 200),
        #     size=(256, 256))
        # self.add_widget(self.image)

        # self.hangman = Label(text=str(self.center_y)+"..." +
        #     str(callback_pos(self, self.pos)))
        # self.add_widget(self.hangman)

        if self.x%2 == 0:
            hangman_img = 'logo-kivy.png'
        else:
            hangman_img = 'green.png'

        self.hangman = Image(source=hangman_img)
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
        self.okbutton.bind(on_press=self.callback)

    def callback(self, value):
        print(self.currenttext)
        self.parent.drawblock.wrongletters.text += self.currenttext
        self.userinput.text = ''

    def on_text(self, memaddress, content):
        print('The widget', content, 'have:', memaddress)
        self.currenttext = content

class GridLangRow(GridLayout):
    """2nd level grid for row with language selector.

    Only the left side of the row should be used for language selection."""
    def __init__(self, **kwargs):
        super(GridLangRow, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(GridLanguages())
        self.add_widget(Label(text=''))

class GridLanguages(GridLayout):
    """3rd level grid for the actual language selector."""
    def __init__(self, **kwargs):
        super(GridLanguages, self).__init__(**kwargs)
        self.cols = 2
        self.lang1 = ToggleButton(text = "EN",
            group = "language", state = "down", text_size=(10, 10))
        self.lang2 = ToggleButton(text = "DE",
            group = "language", background_color=(1,0.5,0.5,1))
        self.add_widget(self.lang1)
        self.add_widget(self.lang2)

class GridInfoExit(GridLayout):
    """2nd level grid for row with Info button and Exit button."""
    def __init__(self, **kwargs):
        super(GridInfoExit, self).__init__(**kwargs)
        self.cols = 2
        self.infobutton = Button(text='Info', font_size=14)
        self.add_widget(self.infobutton)
        self.infobutton.bind(on_press=self.callback)

        # self.exitbuttonwidget = Widget()
        # self.exitbutton = Button(text='Exit game', font_size=14)
        # self.add_widget(self.exitbutton)

        self.exitbutton = Button(text='Exit game', font_size=14)
        self.add_widget(self.exitbutton)


    def callback(self, value):
        print("this is the info button")
        #print(self.userinput.text)

class MainGrid(GridLayout):
    """1st level grid. The main grid of the app.

    This is where ALL the labels, buttons, inputs etc. go."""
    def __init__(self, **kwargs):
        super(MainGrid, self).__init__(**kwargs)
        self.cols = 1

        # title widget
        self.title = Label(text='Hangman')
        self.add_widget(self.title)

        # subtitle widget
        self.subtitle = Label(text='Some more [ref=text]info[/ref] on the game...', markup=True)
        self.subtitle.bind(on_ref_press=print_it)
        self.add_widget(self.subtitle)

        # the word to be guessed
        self.worddisplay = Label(text='------------------ (x letters)')
        self.add_widget(self.worddisplay)

        # needs two cols
        #
        self.hangmanrow = GridHangmanRow()
        self.add_widget(self.hangmanrow)

        # needs 2 cols
        self.languagerow = GridLangRow()
        self.add_widget(self.languagerow)

        # needs 2 cols
        self.exitrow = GridInfoExit()
        self.add_widget(self.exitrow)

if __name__ == '__main__':
    m = MyApp().run()
