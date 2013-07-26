# Make Hangman playable on different devices
# with Kivy http://kivy.org/

import random
import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import *
from kivy.core.image import Image

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

class ShowImage(Image):
   pass

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
        self.add_widget(GridHangman())
        self.add_widget(GridUserInput())

class GridHangman(GridLayout):
    """3rd level grid for Hangman graphic."""
    def __init__(self, **kwargs):
        super(GridHangman, self).__init__(**kwargs)
        self.rows = 2

        # this is a hot mess / in-progress work ;)

        # self.image = ShowImage(source='logo-kivy.png', pos=(200, 200),
        #     size=(256, 256))
        # self.add_widget(self.image)

        self.hangman = Label(text=str(self.center_y)+"..." +
            str(callback_pos(self, self.pos)))
        self.add_widget(self.hangman)

        self.add_widget(Label(text='wrong letters go here'))
        self.bind(pos=callback_pos)

class GridUserInput(GridLayout):
    """3rd level grid for user input and OK button.

    Features and input field for the letter the user wants to guess and a
    button to confirm the input."""
    def __init__(self, **kwargs):
        super(GridUserInput, self).__init__(**kwargs)
        self.rows = 2
        self.userinput = TextInput(multiline=False)
        self.add_widget(self.userinput)
        self.userinput = Button(text='OK', font_size=14)
        self.add_widget(self.userinput)

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
            group = "language", state = "down")
        self.lang2 = ToggleButton(text = "DE",
            group = "language")
        self.add_widget(self.lang1)
        self.add_widget(self.lang2)

class GridInfoExit(GridLayout):
    """2nd level grid for row with Info button and Exit button."""
    def __init__(self, **kwargs):
        super(GridInfoExit, self).__init__(**kwargs)
        self.cols = 2
        self.buttoninfo = Button(text='Info', font_size=14)
        self.add_widget(self.buttoninfo)

        self.buttonexit = Button(text='Exit game', font_size=14)

class MainGrid(GridLayout):
    """1st level grid. The main grid of the app.

    This is where ALL the labels, buttons, inputs etc. go."""
    def __init__(self, **kwargs):
        super(MainGrid, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text='Hangman'))
        self.infolabel = Label(text='Some more [ref=text]info[/ref] on the game...', markup=True)

        # show position
        self.infolabel.bind(on_ref_press=print_it)
        self.add_widget(self.infolabel)

        self.add_widget(Label(text='------------------ (x letters)'))

        # needs two cols
        self.add_widget(GridHangmanRow())

        # needs 2 cols
        self.add_widget(GridLangRow())

        # needs 2 cols
        self.add_widget(GridInfoExit())

if __name__ == '__main__':
    m = MyApp().run()
