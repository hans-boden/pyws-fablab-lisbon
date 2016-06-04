# python3
"""
    Try to import and run a Kivy App
"""

import basicgui as app

class G():
    cons = lambda msg: print(msg)
    msg = lambda msg: print(msg)

def main():
    app.config(dict(title="Importer", cmdhdl=command_handler,
                    inithdl=init_handler))
    app.start()

def init_handler(text):
    print("imp_init_handler: {}".format(text))
    app.put_console('~clr~')
    app.put_console('Welcome to the Kivy world')

    app.put_message('~clr~')

def term_handler(text):
    print("imp_term_handler: {}".format(text))

def command_handler(text):
    print("imp_received text: {}".format(text))
    app.put_console("console text")
    app.put_message("message text")

if __name__ == '__main__':
    main()
