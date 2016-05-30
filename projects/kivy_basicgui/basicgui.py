# python3
"""
    Kivy application to replace commandline interfaces
    It tries to provide a nice GUI for simple interactions with a user
    The module is importable and has a simple programming interface
"""
from kivy.config import Config   # change config before importing other stuff
Config.set('kivy', 'exit_on_escape', 0)  # disable pgm termination with [esc]

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder

kv_text = '''
<BasicGui>:
    itext: txt_input

    orientation: 'vertical'
    padding: 4
    spacing: 4
    canvas.before:
        Color:
            rgb: 0.2, 0.3, 0.7
        Rectangle:
            size: self.size
            pos: self.pos

    Label:
        font_size: 28
        color: 1, 1, 0.5, 1
        size_hint_y: None
        height: 40
        text: root.title_text

    RelativeLayout:
        id: relayo
        pos_hint: {'x': 0.02, 'y': 0.04}  # who understands this?
        size_hint: 0.98, 0.98

        ScrollView:
            pos_hint: {'left': 0.05, 'y': 0.05}
            size_hint: 0.49, 0.90
            canvas.before:
                Color:
                    rgb: 0.8, 0.85, 0.9
                Rectangle:
                    size: self.size
                    pos: self.pos
            Label:
                id: lbl1
                font_size: 16
                color: 0, 0, 0, 1
                padding: (10,5)
                size_hint_y: None
                height: self.texture_size[1]
                text_size: self.width, None
                text: root.label1_text
                valign: 'top' 
        ScrollView:
            pos_hint: {'x': 0.50, 'top': 0.95}
            size_hint: 0.49, 0.90
            canvas.before:
                Color:
                    rgb: 1.0, 1.0, 0.4
                Rectangle:
                    size: self.size
                    pos: self.pos
            Label:
                font_name: 'Consolas'
                font_size: 20
                color: 0, 0, 0, 1
                padding: (10,5)
                size_hint_y: None
                height: self.texture_size[1]
                text_size: self.width, None
                text: root.label2_text
    TextInput:
        id: txt_input
        font_size: 24
        height: 40
        size_hint_y: None
        size_hint_x: 1
        multiline: False
        on_text_validate: root.get_input(self.text)
'''

class G():
    root = None
    title = "Replaceable Title"  
    cmdhdl = lambda text: print("dummy cmdhdl: {}".format(text))
    inithdl = lambda text: print("dummy inithdl: {}".format(text))
    put_cons = lambda text: print("dummy putcons: {}".format(text))
    put_msg = lambda text: print("dummy putmsg: {}".format(text))
    # font files copied manually from the windows font directory
    kivy_fonts = [{
            "name": "Consolas",
            "fn_regular": "data/fonts/consola.ttf",
            "fn_bold": "data/fonts/consolab.ttf",
            "fn_italic": "data/fonts/consolai.ttf",
            "fn_bolditalic": "data/fonts/consolaz.ttf"
    }]


def main():
    for font in G.kivy_fonts:
        LabelBase.register(**font)
    Window.size = (900, 600)
    Builder.load_string(kv_text)

    G.app = ScrollApp()
    G.app.run()

def terminate(dt=None):
    if dt is None:  # direct call from app
        Clock.schedule_once(terminate, 0.1)  # 0.0==immediately is allowed
    else:   # call from clock
        G.app.stop()

class ScrollApp(App):
    def build(self):
        self.title = "Basic Kivy Gui"  # this is the window title
        self.icon = 'user_ico.png'
        root = BasicGui()
        G.root = root  # this allows access to the properties
        return root

    def on_start(self):
        G.inithdl("call from on_start")
        G.root.title_text = G.title

class BasicGui(BoxLayout):
    label1_text = StringProperty('console output')
    label2_text = StringProperty('message output')
    title_text = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("basicGui init()")
        Clock.schedule_once(self.refocus, 0.1)

    def get_input(self, *args):
        newtext = str(args[0])
        if newtext == 'exit':
            terminate()
            return
        self.ids.txt_input.text = ''
        G.cmdhdl(newtext)
        Clock.schedule_once(self.refocus, 0.1)
        return

    def refocus(self, dt):
        self.ids.txt_input.focus = True

#==============================================

def config(kwargs):
    for key, value in kwargs.items():
        if key in 'title cmdhdl inithdl termhdl'.split():
            setattr(G, key, value)
            
def get_console_window():
    return console_updater

def get_message_window():
    return message_updater

def console_updater(text):
    #label_updater(G.root.label1_text, text)
    #return
    if text == '~clr~':
        G.root.label1_text = ''
        return
    G.root.label1_text = G.root.label1_text + text + '\n'

def message_updater(text):
    if text == '~clr~':
        G.root.label2_text = ''
        return
    G.root.label2_text = G.root.label2_text + text + '\n'

def label_updater(lbl, text):
    if text == '~clr~':
        lbl = ''
        return
    lbl = lbl + text + '\n'
    
if __name__ == "__main__":
    main()

