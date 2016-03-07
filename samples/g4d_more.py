# python3
"""
    Demonstrate the use the Gui4Drawings class
"""
import gui4drawing as g4d


def main():

    g = MyGui()


class MyGui(g4d.Gui4Drawing):

    def __init__(self, title='MyGui' ):
        super().__init__(app_title=title, dim=(800,600))
        self.set_zoom(4)
        self.gui_start()

    def _cmd_go(self, argstr):
        """ set a new "current" position (x,y) """
        x, y = self.get_two_ints(argstr)
        if self.check_x(x) and self.check_y(y):
            self.posx, self.posy = x, y

    def _cmd_p(self, argstr):
        """ set a point at the current position """
        self.point()

    def _cmd_color(self, argstr):
        """ set a new color (rgb)"""
        r, g, b = self.get_three_ints(argstr)
        self.color = r, g, b

    def _cmd_zoom(self, argstr):
        """ set a new zoom factor (int) """
        newzoom = int(argstr)
        self.set_zoom(newzoom)

    def _cmd_up(self, argstr):
        newpos = self.posy - int(argstr)
        if self.check_y(newpos):
            for y in range(newpos, self.posy, 1):
                self.pixels[self.posx, y] = self.color
            self.posy = newpos

    def _cmd_down(self, argstr):
        newpos = self.posy + int(argstr)
        if self.check_y(newpos):
            for y in range(newpos, self.posy, -1):
                self.pixels[self.posx, y] = self.color
            self.posy = newpos

    def _cmd_left(self, argstr):
        newpos = self.posx - int(argstr)
        if self.check_x(newpos):
            for x in range(newpos, self.posx, 1):
                self.pixels[x, self.posy] = self.color
            self.posx = newpos

    def _cmd_right(self, argstr):
        newpos = self.posx + int(argstr)
        if self.check_x(newpos):
            for x in range(newpos, self.posx, -1):
                self.pixels[x, self.posy] = self.color
            self.posx = newpos

    def _cmd_absto(self, argstr):
        """ Draw a line to absolute position (x,y)"""
        x, y = self.get_two_ints(argstr)
        if self.check_x(x) and self.check_y(y):
            self.draw_line(self.posx, self.posy, x, y)

    def _cmd_relto(self, argstr):
        """ Draw a line to relative position (x,y)"""
        x, y = self.get_two_ints(argstr)
        x += self.posx
        y += self.posy
        if self.check_x(x) and self.check_y(y):
            self.draw_line(self.posx, self.posy, x, y)

    def _cmd_test(self, argstr):
        self.put_msg("Color: {}".format(str(self.color)))
        self.put_msg("Visible: {}".format(str(self.visible)))
        self.put_msg("Current: {}, {}".format(self.posx, self.posy))

    def draw_line(self, x1, y1, x2, y2):
        for x, y in g4d.line_pixels(x1, y1, x2, y2):
            self.pixels[x, y] = self.color
        self.posx = x2
        self.posy = y2

    def check_x(self, posx):
        if 0 <= posx < self.visible[0]:
            return True
        self.put_msg("Coords outside visible area")
        return False

    def check_y(self, posy):
        if 0 <= posy < self.visible[1]:
            return True
        self.put_msg("Coords outside visible area")
        return False

    def point(self):
        self.pixels[self.posx, self.posy] = self.color

    def get_two_ints(self, str):
        str = str.replace(',', ' ')
        x, y = str.split()
        return int(x), int(y)

    def get_three_ints(self, str):
        str = str.replace(',', ' ')
        r, g, b = str.split()
        return int(r), int(g), int(b)


main()
