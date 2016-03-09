"""
The DynamicDisplay class is instantiated with an image (Pillow(PIL) is required).
This image is displayed on a tkinter canvas repeatedly, until a completed flag becomes True.
The main process updates the image at any time, and the changes are visible in "real time".
The fps parameter is  used to calculate the time between 2 display operations. For larger
images, only a low  fps rate is possible.

The test() function shows the usage of the module.
"""
import tkinter as tk
from tkinter.filedialog import asksaveasfilename
from PIL import Image, ImageTk
import os.path
from threading import Thread
import time


class DynamicDisplay():
    def __init__(self, pilim, fps=5, title="Gui for an Image"):
        self.im = pilim
        self.title = title
        self.tkimg = None
        self.cnvs_ref = None
        self.event_ref = None
        self.waittime = int(1000 / min(fps, 25))  # milliseconds
        print("Requested time per frame: {:4.1f}ms".format(self.waittime))

        self.global_start = time.time()
        self.showcount = 0
        self.showtime = 0.0

        print('image:', self.im)

        gui_thread = Thread(target=self.gui)
        gui_thread.start()

    def terminate(self):
        #print('termination, cancel id:', self.event_ref)
        self.mainw.after_cancel(self.event_ref)
        self.mainw.quit()

    def show(self):
        start = time.time()
        if self.cnvs_ref:  # delete previous image from canvas
            self.canvas.delete(self.cnvs_ref)
        self.tkimg = ImageTk.PhotoImage(self.im)
        self.cnvs_ref = self.canvas.create_image(10,10, anchor=tk.NW, image=self.tkimg)
        #print('im:', self.im,' evt_id:', self.event_ref)
        used_time = 1000 * (time.time() - start)  # ms
        self.showtime += used_time
        self.showcount += 1

        if not getattr(self.im, 'completed', False):
            actual_wait = max(10.0, self.waittime - used_time)
            self.event_ref = self.mainw.after(int(actual_wait), self.show) # schedule next call
            return

        now = time.time()
        fps = self.showcount/(now-self.global_start)
        print("Total time for loop: {:1.2f} s".format(now-self.global_start))
        print("Total time required for display: {:1.2f} s".format(self.showtime/1000))
        print("Actual frames per second displayed: {:1.1f}".format(fps))
        print("Average time for update: {:1.1f} ms".format(self.showtime/self.showcount))

    def save_as(self):
        name = asksaveasfilename(parent=self.mainw, initialfile=self.title,
                                 filetypes=[('Portable Network Graphic', '*.png')])
        if name.strip() == '':
            return
        base, ext = os.path.splitext(name)
        if ext == '':
            name += '.png'
        self.im.save(name)
        print("saved as", name)

    def gui(self):
        cnv_dimx, cnv_dimy = [x+20 for x in self.im.size]

        self.mainw = tk.Tk()
        self.mainw.title(self.title)
        self.mainw.protocol("WM_DELETE_WINDOW", self.terminate)

        menubar = tk.Menu(self.mainw)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save as...", command=self.save_as)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.terminate)
        menubar.add_cascade(label="File", menu=filemenu)
        self.mainw.config(menu=menubar)
        
        self.canvas = tk.Canvas(self.mainw, width=cnv_dimx, height=cnv_dimy)
        self.canvas.pack()

        self.show()

        tk.mainloop()


def test():

    im = Image.open('resources/sample.jpg')
    im.completed = False  # inject some flag into the image object
    pixels = im.load()  # PixelAccess object, load before starting gui

    gui = DynamicDisplay(im, fps=16, title="test image")
    dimx,dimy = im.size

    time.sleep(1.0)
    print('start pixel loop')
    for posy in range(dimy):
        time.sleep(0.01)
        for posx in range(dimx):
            red = 20 + posx % 200
            grn = 40 + posy % 180
            blu = 60 + (posx+posy) % 150
            pixels[posx, posy] = (red, grn, blu)

    im.completed = True
    print('test ended')

if __name__ == '__main__':
    test()
