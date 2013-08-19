# -*- coding: utf-8 -*-
# Trying out things with Kivy

import kivy
kivy.require('1.7.1') # replace with your current kivy version !

# from kivy.config import Config
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

from kivy.core.text import LabelBase
from kivy.utils import escape_markup


class TestApp(App):
    """Main app."""
    def build(self):
        return AppBody()

class AppBody(FloatLayout):
    """Body of the app."""
    def __init__(self, **kwargs):
        super(AppBody, self).__init__(**kwargs)
        initialheight = Window.height
        initialwidth = Window.width

        newheight = self.bind(height=self.callback_pos)
        self.bind(width=self.callback_pos)

        print("new height: ", newheight)

        print("the height is: ", str(thisheight), "the width is: ", str(thiswidth), "position is: ", str(thisposition))

        text28 = 28

        # text28_resized = (newheight*text28)/defaultwidth



        # self.layout = FloatLayout(size=(300, 300))

        labeltitle = Label(text="[size=24][b]" + escape_markup("Hangman Game")
            + "[/b][/size]", markup=True, size_hint=(.4, .1),
                pos_hint={'x':0.3, 'y':0.9})
        labelsubtitle = Label(text="Guess the word!", size_hint=(.4, .1),
                pos_hint={'x':0.3, 'y':0.83})


        imgsource = 'images/hangman-1-dead.png'
        # self.imageliste = glob.glob('images/*.png')

        labelblankword = Label(text="[size=28][b]" + escape_markup("_ A _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
            + "[/b][/size]", markup=True, size_hint=(.6, .1), pos_hint={'x':0.2, 'y':0.7})


        hangmanpic = Image(source=imgsource, size_hint=(.5, .7), pos_hint={'x':-0.02, 'y':0.1})
        self.add_widget(hangmanpic)

        textinput = TextInput(text='', multiline=False, focus=True,
            size_hint=(.2, .102), pos_hint={'x':0.61, 'y':0.4})
        buttonok = Button(text='OK', size_hint=(.2, .1),
                pos_hint={'x':0.79, 'y':0.4})

        labelwrongguesses = Label(text="" + escape_markup("A, B, C")
            + "", markup=True, size_hint=(.6, .1), pos_hint={'x':0, 'y':0.1})


        buttonsettings = Button(text='Settings', size_hint=(.5, .1),
                pos_hint={'x':0.0, 'y':0})
        buttonexit = Button(text='Exit', size_hint=(.5, .1),
                pos_hint={'x':0.5, 'y':0})


        self.add_widget(labeltitle)
        self.add_widget(labelsubtitle)
        self.add_widget(labelblankword)

        self.add_widget(textinput)
        self.add_widget(buttonok)

        self.add_widget(labelwrongguesses)

        self.add_widget(buttonsettings)
        self.add_widget(buttonexit)



    def callback_pos(self, instance, *args):
        """Give back the value of a certain position."""
        self.newheight = args
        print("self new heigh isssss: ", self.newheight)
        return self.newheight

        # self.textinput.bind(text=self.onLetterInput)



if __name__ == '__main__':
    TestApp().run()

# class MyApp(App):

#     def build(self):
#         return Label(text='Hello world')

# if __name__ == '__main__':
#     MyApp().run()
