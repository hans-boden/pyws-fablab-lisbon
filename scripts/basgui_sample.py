# python 3
""" use a gui module as our user interface
    implement some application by extending the text_input() function
"""

import basic_gui

class G():
    appgui = None

def main():
    G.appgui = basic_gui.CmdlAppGui("Title Text", text_input)
    G.appgui.start()

def text_input(text):
    print("received input: '{}'".format(text))
    G.appgui.put_msg("> {}\n".format(text))
    G.appgui.put_data("response to '{}'\n".format(text), style=1)

    if text == 'exit':
        G.appgui.finish()

main()

    
