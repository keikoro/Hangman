# Make Hangman playable on different devices
# with Kivy http://kivy.org/

from __future__ import print_function # for python2.x
import random
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

# class ShowImage(Image):
#    pass


class HangmanApp(App):
    """Main app."""
    def build(self):
        # return Label(text='Hello world')
        return MainGrid()

    # def on_start(self):
    #     print("ich starte")
    #     self.info_popup()


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
        # this is a hot mess / in-progress work ;)

        # self.image = ShowImage(source='logo-kivy.png', pos=(200, 200),
        #     size=(256, 256))
        # self.add_widget(self.image)

        # self.hangman = Label(text=str(self.center_y)+"..." +
        #     str(callback_pos(self, self.pos)))
        # self.add_widget(self.hangman)

        # if self.x%2 == 0:
        #     hangman_img = 'logo-kivy.png'
        # else:
        #     hangman_img = 'green.png'

#        self.imgsource = self.parent.img1

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
        self.okbutton.bind(on_press=self.callback)

    def callback(self, value):
        print(self.currenttext)

        self.parent.drawblock.hangman.source = random.choice(self.parent.imageliste)

        # wrong letters
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
        print("voice: ", self.parent.voice, ", language: ", self.parent.language)


class MainGrid(GridLayout):
    """1st level grid. The main grid of the app.

    This is where ALL the labels, buttons, inputs etc. go."""
    def __init__(self, **kwargs):
        super(MainGrid, self).__init__(**kwargs)
        self.voice = False
        self.language = 'en'
        self.cols = 1

        # title widget
        self.title = Label(text='Blblbllablbl text here')
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

        # # needs 2 cols
        # self.languagerow = GridLangRow()
        # self.add_widget(self.languagerow)

        # needs 2 cols
        self.exitrow = GridInfoExit()
        self.add_widget(self.exitrow)

        Clock.schedule_once(self.settings_popup, 1)

#        self.info_popup()

        # open the text-to-speech selection popup
        # self.settings_popup()

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

        content.add_widget(Label(text='Here you can change the settings\n'
            'of the game', height='100sp'))
        content.add_widget(voiceon)
        content.add_widget(voiceoff)
        content.add_widget(lang_en)
        content.add_widget(lang_de)
        content.add_widget(closebutton)

        self.popup = Popup(content=content, title='Hangman settings',
                      size_hint=(None, None), size=('300dp', '400dp'))

        closebutton.bind(on_release=self.close_popup)
        voiceon.bind(on_release=self.voice_on)
        voiceoff.bind(on_release=self.voice_off)
        lang_en.bind(on_release=self.pick_lang_en)
        lang_de.bind(on_release=self.pick_lang_de)

        # voiceon.bind(on_release=self.voice_on)
        # voiceoff.bind(on_release=self.voice_off)

        # button = Button(text='Open popup', size_hint=(None, None),
        #                 size=('150dp', '70dp'),
        #                 on_release=popup.open)

        self.popup.open()
        col = AnchorLayout()
        # col.add_widget(button)
        return col

    def pick_lang_en(self, bla):
        self.language = 'en'
        print("language: ", self.language)

    def pick_lang_de(self, bla):
        self.language = 'de'
        print("language: ", self.language)

    def voice_on(self, bla):
        self.voice = True
        print("voice: ", self.voice)

    def voice_off(self, bla):
        self.voice = False
        print("voice: ", self.voice)

    def close_popup(self, bla):
        self.popup.dismiss()

    # def voice_on(self, bla):
    #     self.voice = True
    #     print("voice: ", self.voice)
    #     self.popup.dismiss()

    # def voice_off(self, bla):
    #     self.voice = False
    #     print("voice: ", self.voice)
    #     self.popup.dismiss()

if __name__ == '__main__':
    m = HangmanApp().run()
