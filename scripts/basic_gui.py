#! python3
""" Basic GUI to replace command line IO for simple applications
    This is the GUI-Module (v.2)
"""

import tkinter as tk
from  tkinter import ttk
from  tkinter.scrolledtext import ScrolledText

class CmdlAppGui(object):
    def __init__(self, title, cb_input):
        self.title = title
        self.cb_input = cb_input
        self.here = False

        self.root = tk.Tk()
        self.root.title(title)
        self.frm = ttk.Frame(master=self.root, padding="3 3 12 12")

        self.build(self.frm)
        self.here = True


    def start(self):
        self.frm.mainloop()
        self.here = False

        #self.cb_input("message9")
        
    def put_msg(self, text, style=0):
        if self.here:
            if style == 1:
                self.scrollmsg.insert(tk.INSERT, text, 'bold')
            else:
                self.scrollmsg.insert(tk.INSERT, text, '')
            self.scrollmsg.yview_scroll(99,'pages')
        else:
            print("GUI: {0}".format(text))

    def put_data(self, text, style=0):
        if self.here:
            if style == 1:
                self.scrolldata.insert(tk.INSERT, text, 'bold')
            else:
                self.scrolldata.insert(tk.INSERT, text, '')
            self.scrolldata.yview_scroll(99,'pages')
        else:
            print("GUI: {0}".format(text))

    def build(self, frm):
        frm.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        frm.columnconfigure(0, weight=1)
        frm.columnconfigure(1, weight=2)
        frm.rowconfigure(0, weight=1)

        self.scrollmsg = ScrolledText(frm, wrap=tk.WORD, width=40)
        self.scrollmsg.grid(column=0, row=1, sticky="EW")
        self.scrollmsg.tag_config('bold', font=('Courier',10,'bold'))
        
        self.scrolldata = ScrolledText(frm, wrap=tk.WORD, width=40)
        self.scrolldata.grid(column=1, row=1, rowspan=9, sticky="NS")
        self.scrolldata.tag_config('bold', font=('Courier',10,'bold'))
        
        self.entrytext = tk.StringVar()
        self.entry = ttk.Entry(frm, textvariable=self.entrytext)
        self.entry.grid(column=0, row=3, sticky='EW')
        self.entry.bind("<Return>", self.on_press_enter)

        btn_quit = ttk.Button(frm, text="QUIT",
                            command=self.finish)
        btn_quit.grid(column=0,
                            row=9, sticky="EW")

        for child in frm.winfo_children():
            child.grid_configure(padx=5, pady=5)
            
        self.entry.focus_set() # set the focus on the entry field

    def on_press_enter(self, event):
        text = self.entrytext.get()
        self.cb_input(text)

        if self.here:
            self.entrytext.set('')
            self.entry.focus_set() # set the focus on the entry field

    def finish(self):  # program call to terminate GUI
        self.here = False
        self.entry.unbind("<Return>")
        self.root.destroy()


def test():
    def text_input(text):
        # print("received input: '{text}'".format(text=text))
        appgui.put_msg("> {0}\n".format(text))
        appgui.put_data("response to '{resp}'\n".format(resp=text), style=1)

    appgui = CmdlAppGui("Title Text", text_input)
    #time.sleep(1)
    appgui.start()


if __name__ == '__main__':
    print("test start")
    test()
    print("test ended")

