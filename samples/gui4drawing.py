# python3
"""
    This defines a class which provides a generic gui for drawing

    The final application subclasses the Gui4Drawing class and implements its own
    command handler

    The drawing goes to a PIL image which is displayed on a tkinter canvas
"""
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import asksaveasfilename
import os, os.path
from PIL import Image, ImageTk



def main():
    mygui = MyGui('test gui')




class Gui4Drawing():
    def __init__(self, app_title='Gui4Drawing', dim=(800,400)):
        self.title = app_title
        self.imgdim = dim
        self.gui = GenericGui(self, app_title = self.title, dim=dim)

        self.put_msg = self.gui.put_msg  # import gui method
        self.quit = self.gui.finish
        self.quit_cmd = 'x'

        self.local_cmds = self.find_cmds()

        self.image = Image.new("RGB", self.imgdim)
        self.pixels = self.image.load()

        # tool attibutes
        self.zoom_factor = 6
        self.visible = self.calc_visible_area(self.image, self.zoom_factor)
        self.posx = self.posy = 0
        self.pen_down = False
        self.color = (200,200,200)


    def gui_start(self):
        self.show_image()
        self.show_status()

        self.gui.start()

    def set_zoom(self, zoom_factor):
        if 1 <= zoom_factor <= 8:
            self.zoom_factor = zoom_factor

        self.calc_visible_area(self.image, self.zoom_factor)
        return self.zoom_factor

    def calc_visible_area(self, img, zoomf):
        dimx, dimy = img.size
        cropx = dimx // zoomf
        cropy = dimy // zoomf
        return cropx, cropy


    def cb_input(self, text):
        if text.strip() == self.quit_cmd:

            self.quit()
            return

        try:
            result = self.exec_method(text.strip())
        except Exception as excp:
            self.put_msg("command '{}' failed: {}".format(text, str(excp)))
            return

        if not result is None:
            self.put_msg(str(result))
        self.show_image()
        self.show_status()

    def show_image(self):
        im = self.image
        if self.zoom_factor > 1:
            im = self.zoom(im, self.zoom_factor)
        self.gui.show_image(im)

    def show_status(self):
        text = []
        dimx, dimy = self.calc_visible_area(self.image, self.zoom_factor)
        text.append("VisibleArea: ({}, {})".format(dimx, dimy))
        text.append("Position: ({}, {})".format(self.posx, self.posy))
        r,g,b = self.color
        text.append("Color(rgb): ({}, {}, {})".format(r,g,b))
        text.append("ZoomFactor: ({})".format(self.zoom_factor))
        self.gui.show_status('\n'.join(text))

    def zoom(self, img, zoomf):
        cropx, cropy = self.calc_visible_area(img, zoomf)
        newx = cropx * zoomf
        newy = cropy * zoomf
        l,u,r,b = 0, 0, cropx, cropy
        box = (l,u,r,b)
        cropimg = self.image.crop(box)
        resized = cropimg.resize((newx, newy))

        return resized
    def find_cmds(self):
        names = [x[5:] for x in dir(self) if x.startswith('_cmd_')]
        return names

    def exec_method(self, text):
        for name in self.local_cmds:
            if text.startswith(name):
                break
        else:
            raise ValueError('command not defined')

        meth = self.__class__.__dict__['_cmd_'+name]
        rest = text[len(name):].strip()

        return meth(self, rest)


class GenericGui():
    def __init__(self, app, app_title, dim):
        self.app = app  # this is the main application object
        self.title = app_title
        self.image = None
        self.imgdim = dim
        self.root = tk.Tk()
        self.root.title(app_title)
        self.root.protocol("WM_DELETE_WINDOW", self.finish)
        self.frm = ttk.Frame(master=self.root, padding="3 3 3 3")
        self.build(self.root, self.frm)
        self.cnvs_ref = None
        self.on = True


    def start(self):
        self.entry.focus_set() # set the focus on the entry field
        self.frm.mainloop()
        self.on = False

    def finish(self):  # program call to terminate GUI
        self.entry.unbind("<Return>")
        self.root.destroy()
        self.on = False

    def put_msg(self, text, style=0, end='\n'):
        if self.on:
            if style == 1:
                self.scrollmsg.insert(tk.INSERT, text+end, 'bold')
            else:
                self.scrollmsg.insert(tk.INSERT, text+end, '')
            self.scrollmsg.yview_scroll(99,'pages')
        else:
            print("GUI: {0}".format(text))


    def on_press_enter(self, event):
        text = self.entrytext.get()
        self.app.cb_input(text)

        if self.on:
            # self.put_msg('>>> {}\n'.format(text))

            self.entrytext.set('')
            self.entry.focus_set() # set the focus on the entry field

    def save_as(self):
        name = asksaveasfilename(parent=self.root, initialfile=self.title,
                                 filetypes=[('Portable Network Graphic', '*.png')])
        if name.strip() == '':
            return
        base, ext = os.path.splitext(name)
        if ext == '':
            name += '.png'
        self.image.save(name)

    def show_image(self, image):
        if self.cnvs_ref:
            self.canvas.delete(self.cnvs_ref)
        self.image = image  # keep local copy for 'save'
        self.tkimg = ImageTk.PhotoImage(image)
        self.cnvs_ref= self.canvas.create_image(10, 10, anchor=tk.NW, image=self.tkimg)

    def show_status(self, text):
        self.txt_status.configure(state='normal')
        self.txt_status.delete('1.0', 'end')
        self.txt_status.insert('end', text)
        self.txt_status.configure(state='disabled')

    def build(self, root, frm):
        frm.grid(column=0, row=0, sticky=("NEWS"))
        frm.columnconfigure(0, weight=2)
        frm.rowconfigure(0, weight=2)
        frm.rowconfigure(1, weight=1)

        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save as...", command=self.save_as)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.finish)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

        cnv_dimx, cnv_dimy = [x+20 for x in self.imgdim]

        self.canvas = tk.Canvas(self.frm, width=cnv_dimx, height=cnv_dimy)
        self.canvas.grid(column=0, row=0, columnspan=2)

        self.scrollmsg = ScrolledText(frm, wrap=tk.WORD, width=40, height=10)
        self.scrollmsg.grid(column=0, row=1, sticky="NEWS")
        self.scrollmsg.tag_config('bold', font=('Courier',10,'bold'))

        self.entrytext = tk.StringVar()
        self.entry = ttk.Entry(frm, textvariable=self.entrytext)
        self.entry.grid(column=0, row=2, sticky='EW')
        self.entry.bind("<Return>", self.on_press_enter)

        self.btn_quit = ttk.Button(frm, text='Quit', command = self.finish)
        self.btn_quit.grid(column=1, row=2, sticky="EW")

        self.txt_status = tk.Text(frm, width=30, height=5)
        self.txt_status.grid(column=1, row=1, sticky="N")

class MyGui(Gui4Drawing):
    def __init__(self, title='MyGui'):
        super().__init__(app_title=title)

        self.pixels[3,3] = (200,200,200)
        self.pixels[3,4] = (200,200,200)
        self.pixels[4,4] = (200,200,200)

        self.gui_start()

    def _cmd_go(self, argstr):
        x, y = self.get_two_ints(argstr)
        self.posx, self.posy = x, y


    def _cmd_p(self, argstr):
        self.point()

    def point(self):
        self.pixels[self.posx, self.posy] = self.color

    def get_two_ints(self, str):
        str = str.replace(',', ' ')
        x, y = str.split()
        return int(x), int(y)



def line_pixels(x1,y1,x2,y2):
    # a generator: generate pixel coordinates between and including the two end points
    if abs(x2-x1) > abs(y2-y1):
        yield from line_pixels_norm(x1,y1,x2,y2)
    else:
        yield from exchg(line_pixels_norm(y1,x1,y2,x2))

def exchg(gener):
    for a, b in gener:
        yield b, a

def line_pixels_norm(a1, b1, a2, b2):
    # assumption: a > b
    # generate a coordinate pair for both end points
    stepa = 1 if a2 > a1 else -1
    stepb = 1 if b2 > b1 else -1 if b1 > b2 else 0
    round = 0.5 - 0.001 * stepb
    diffa = a2 - a1 + stepa
    offsb = (b2-b1+stepb) / diffa*stepa
    for a in range(0, diffa, stepa):
        b = abs(a) * offsb
        yield a1+a, int(b1+b+round)

def test():
    coords = ((2,2, 8,2), (2,8, 2,2), (8,2, 2,2), (2,2, 2,8),
              (9,9, 13,15),(9,9, 15,13), (9,9, 13,4), (9,9, 16,6),
              (9,9, 2,6), (9,9, 6,2), (9,9, 2,12), (9,9, 7,16))

    for tup in coords:
        print(tup)
        x1,y1,x2,y2 = tup
        for x,y in line_pixels(x1,y1,x2,y2):
            print("{:2} {:2}".format(x,y))

if __name__ == '__main__':
    #main()
    test()
