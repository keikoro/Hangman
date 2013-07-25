# Make Hangman playable on different devices
# with Kivy http://kivy.org/

import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
# import kivy.app
# import kivy.uix.label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import *

class MyApp(App):
    def build(self):
        # return Label(text='Hello world')
        return MainGrid()

class MiniGrid(GridLayout): # only needed as 'tempate' right now
    def __init__(self, **kwargs):
        super(MiniGrid, self).__init__(**kwargs)
        self.cols = 2
        self.buttoninfo = kivy.uix.button.Button(text='Info', font_size=14)
        self.add_widget(self.buttoninfo)
        #self.add_widget(Label(text='6. Zeile, 2. Spalte'))
        self.buttonexit = kivy.uix.button.Button(text='Exit game', font_size=14)
        self.add_widget(self.buttonexit)

class GridHangmanRow(GridLayout):
    def __init__(self, **kwargs):
        super(GridHangmanRow, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(GridHangman())
        self.add_widget(GridUserInput())

class GridHangman(GridLayout):
    def __init__(self, **kwargs):
        super(GridHangman, self).__init__(**kwargs)
        self.rows = 2
        #self.add_widget(Label(text='bla'))
        # self.canvas.add(Rectangle(size=(50, 50)))

        self.hangman = Label(text='hangman')
        self.add_widget(self.hangman)

        with self.hangman.canvas:
            Color(1., 1., 0)
            Rectangle(size=(50, 50))
        # self.canvas.add(Color(1., 1., 0))
        # self.canvas.add(Rectangle(size=(50, 50)))

        # with self.canvas:
        #     Color(1., 1., 0)
        #     Rectangle(size=(50, 50))

        #     # Add a rectangle
        #     Rectangle(pos=(10, 10), size=(500, 500))


        self.add_widget(Label(text='wrong letters go here'))

class GridUserInput(GridLayout):
    def __init__(self, **kwargs):
        super(GridUserInput, self).__init__(**kwargs)
        self.rows = 2
        self.userinput = TextInput(multiline=False)
        self.add_widget(self.userinput)
        self.buttoneingabe = Button(text='OK', font_size=14)
        self.add_widget(self.buttoneingabe)

class GridLangRow(GridLayout):
    def __init__(self, **kwargs):
        super(GridLangRow, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(GridLanguages())
        self.add_widget(Label(text=''))

class GridLanguages(GridLayout):
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
    def __init__(self, **kwargs):
        super(GridInfoExit, self).__init__(**kwargs)
        self.cols = 2
        self.buttoninfo = kivy.uix.button.Button(text='Info', font_size=14)
        self.add_widget(self.buttoninfo)
        #self.add_widget(Label(text='6. Zeile, 2. Spalte'))
        self.buttonexit = kivy.uix.button.Button(text='Exit game', font_size=14)
        self.add_widget(self.buttonexit)


class MainGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MainGrid, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text='Hangman'))
        self.add_widget(Label(text='Some more info on the game...'))

        self.add_widget(Label(text='------------------ (x letters)'))

        # needs two cols
        self.add_widget(GridHangmanRow())

        # needs 2 cols
        self.add_widget(GridLangRow())

        # needs 2 cols
        self.add_widget(GridInfoExit())

if __name__ == '__main__':
    MyApp().run()
