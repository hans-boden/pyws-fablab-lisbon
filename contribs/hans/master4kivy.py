# python3
"""
    Run the mastermind game inside the kivy basic gui
"""

import basicgui as gui

def main():
    gui.config(dict(title="Mastermind",
                    cmdhdl=command_handler,
                    inithdl= init_handler))
    gui.start()
    pass

def init_handler(text):
    #gui.put_console('~clr~')
    #gui.put_message('~clr~')
    #gui.put_message('Welcome to the game of \'Mastermind\'')
    pass

def command_handler(text):
    guess = check_input(text)
    gui.put_console("input: {}".format(guess))

def check_input(text):
    return text

if __name__ == '__main__':
    main()
