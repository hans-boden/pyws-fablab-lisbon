# python3
"""
    Demonstrate the use the Gui4Drawings class
"""
from gui4drawing import Gui4Drawing


def main():

    g = MyGui()


class MyGui(Gui4Drawing):

    def __init__(self, title='MyGui' ):
        super().__init__(app_title=title, dim=(600,400))
        self.set_zoom(4)
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


main()
