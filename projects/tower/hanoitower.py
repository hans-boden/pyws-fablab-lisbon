# python3
"""
    second steps in learning Kivy - make the towers of hanoi
"""

import time
from queue import Queue

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.vector import Vector
from kivy.graphics import Rectangle, Color
from kivy.lang import Builder

class G():
    disks = {}
    moving = []
    status = True  # callback loop
    pq = Queue()
    dnames = "disk1 disk2 disk3 disk4 disk5 disk6 disk7".split()

    dcols = [120, 360, 600, 480]  # x-pos
    dlevel = [20, 50, 80, 110, 140, 170, 200, 230, 260, 10]   # y-pos
    wsize = [100, 100]  # window size
    dsize = [60, 90, 120, 150, 180, 220, 250]  # disk size (horiz)
    dthick = 20
    speed = 3.0
    solver = None
try:
    import solver
except:
    print("import 'solver.py' failed")
else:
    print("solver:", solver, solver.solver)
    G.solver = solver.solver

def main():
    Builder.load_string(kv_code)
    app = HanoiApp()
    app.run()


class HanoiApp(App):

    def build(self):
        game = HanoiTower()
        Clock.schedule_interval(game.update, 1.0/50.0)
        return game

class HanoiTower(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setup_disks()
        G.pq.put("disk7 0 0")
        G.pq.put("disk6 0 1")
        G.pq.put("disk5 0 2")
        G.pq.put("disk4 0 3")
        G.pq.put("disk3 0 4")
        G.pq.put("disk2 0 5")
        G.pq.put("disk1 0 6")
        #print("start_size: {}".format(str(self.size)))
        # start size is 100,100, but after initialization, newsize
        # is already called with 800,600

    txtin_oprop = ObjectProperty(None)

    def get_input(self, *args):
        print("textInput {}".format(str(args)))
        G.pq.put(self.txtin_oprop.text)
        self.txtin_oprop.text = ''  # clear input field

    def input_focus(self, state):
        # when input looses focus, set it back again
        if state is False:
            print("lost focus")
            #self.txtin_oprop.focus = True

    def new_size(self, size):
        print("new size: {}".format(str(size)))
        G.wsize = size
        w, h = size
        G.dcols = [x * w for x in (0.2, 0.5, 0.8, 0.65)]
        vertoffs = h * 0.06
        vertbase = h * 0.07
        G.dlevel = [vertbase + x * vertoffs for x in range(8)]
        G.dlevel[7] = h *0.04
        G.dsize = [w * 0.1 + w * 0.035 * x for x in range(7)]
        G.dthick = h * 0.05

        print("dcols", G.dcols)
        print("dlvl ", G.dlevel)
        print("dsize", G.dsize)
        self.resize_disks()

    def setup_disks(self):
        G.moving = []
        for seq, name in enumerate(G.dnames):
            disk = self.ids[name]
            disk.set_id(seq, name)

        self.resize_disks()
        return

    def resize_disks(self):
        for name in G.dnames:
            disk = self.ids[name]
            disk.resize()

    def move_to(self, diskid, newc, newl):  # newx, newy are column level positions
        print("move for {}".format(diskid))
        disk = self.ids[diskid]

        disk.move_to(newc, newl)
        G.moving.append(disk)


    def update(self, dt):
        for disk in G.moving[:]:
            if disk.move():
                G.moving.remove(disk)

        if len(G.moving) >= 1: # not more than one disk at a time
            return

        if not G.pq.empty():
            command = G.pq.get()
            print("command: {}".format(command))

            if command == 'solve':
                if G.solver:
                    G.solver(G.pq)
                return

            self.txtin_oprop.focus = True
            try:
                diskid, newc, newl = command.split()
                assert diskid in G.dnames
                newc = int(newc)
                newl = int(newl)
                assert 0 <= newc < 3
                assert 0 <= newl < 7
            except:
                print("bad command:")
            else:
                self.move_to(diskid, newc, newl)


        #if next(self.cbloop):
        #    self.backcall()

        return # G.status

        #print("d6.center: {}, pos: {}, x: {}, y: {}"
        #      .format(self.d6.center, self.d6.pos, self.d6.x, self.d6.y))

        # bounce off top and bottom
        #if (self.ball.y < 0) or (self.ball.top > self.height):
        #    self.ball.velocity_y *= -1

        # bounce off left and right
        #if (self.ball.x < 0) or (self.ball.right > self.width):
        #    self.ball.velocity_x *= -1


class Disk(Widget):
    #pos_hint_x = NumericProperty(20)
    #pos_hint_y = NumericProperty(50)

    # velocity of the ball on x and y axis
    #velocity_x = NumericProperty(10)
    #velocity_y = NumericProperty(0.5)
    # referencelist property so we can use ball.velocity as a shorthand
    #velocity = ReferenceListProperty(velocity_x, velocity_y)

    def __init__(self, **kwargs):

        self.diskid = 'noid'
        self.dcol = 3
        self.dlvl = 7
        self.newx = None
        self.newy = None
        self.oldx = None
        self.oldy = None
        self.posgen = None

        super().__init__(**kwargs)
        pass

    def set_id(self, seqno, name):
        self.seqno = seqno
        self.name = name

    def resize(self):
        print("resize", self.name)
        print("col {}, row {}".format(self.dcol, self.dlvl))

        ndx = self.seqno
        dx, dy = G.dsize[ndx], G.dthick
        self.size = Vector(dx, dy)
        px, py = G.dcols[self.dcol], G.dlevel[self.dlvl]
        self.center = Vector(px,py)

    def move_to(self, newc, newl):
        self.dcol = newc
        self.dlvl = newl
        self.posgen = None
        self.newx = G.dcols[newc]
        self.newy = G.dlevel[newl]
        print("initialize to: {:5.2f}, {:5.2f}".format(self.newx, self.newy))

    def move(self):
        cx, cy = self.center_x, self.center_y
        if self.posgen is None:
            self.oldx = cx
            self.oldy = cy
            self.posgen = gen_smooth(cx,cy, self.newx, self.newy, speed=G.speed)
            print("move old: {:5.2f}, {:5.2f},  new: {:5.2f}, {:5.2f}"
                  .format(self.oldx, self.oldy, self.newx, self.newy))

        try:
            px, py = next(self.posgen)
        except StopIteration:
            return True
        #print("move disk to {:5.2f}, {:5.2f}".format(px, py))

        self.center = Vector(px, py)   # vector + pos, sonst gehts schief


#class Block(Widget):
#    pos_hint_x = NumericProperty(0)
#    pos_hint_y = NumericProperty(0)
#    color = ListProperty([1, 1, 1, 1])
#    proper_color = [.6, .3, .1, 1]
#
#    def __init__(self, x, y):
#        super(Block, self).__init__()
#        self.pos_hint_x = x
#        self.pos_hint_y = y


def gen_cb(loop=20):
    # generator: yields infinite repetitions of 19 False and 1 True
    x = 0
    while True:
        x = (x+1)%loop
        yield not x


def gen_smooth(x1,y1, x2,y2, speed=1.0):
    # generator: yield a sequence of positions between two coordinates
    dx = x2-x1
    dy = y2-y1
    dist = max(abs(dx),abs(dy)) / speed

    movtab = get_smooth_table(dist)

    way = 0
    for d in movtab:
        #print('smooth', d)
        way += d
        quot = way / dist

        yield x1 + dx*quot, y1 + dy*quot

    yield x2, y2


def get_smooth_table(dist, max_step=30):

    movtab = []
    revers = []
    way = 0
    for step in range(1, max_step):
        if way + step <= dist:
            movtab.append(step)
            way += step

        if way + step <= dist:
            revers.append(step)
            way += step
        else:
            break

    while way+max_step < dist:
        movtab.append(max_step)
        way += max_step

    for step in range(max_step-1 , 0, -1):
        if way + step <= dist:
            ndx = revers.index(step)
            revers[ndx:ndx] = [step]
            way += step

    revers.reverse()
    movtab.extend(revers)

    return movtab

kv_code = '''

#:set floor_size_y  15
#:set col_size_x  18

<Disk>:
    size: 200,20
    pos: 1,1
    canvas:
        Color:
            id: disk_color
            rgb: 0.6, 0.0, 0.4
        Rectangle:
            pos: self.pos
            size: self.size

<HanoiTower>:
    on_size: root.new_size(self.size)

    txtin_oprop: txt_input

    BoxLayout:
        orientation: 'vertical'
        size: root.size

        TextInput:
            id: txt_input
            font_size: 24
            height: 40
            size_hint_y: None
            size_hint_x: None
            width: 500
            text: 'command input'
            multiline: False
            on_text_validate: root.get_input(self.text)
            on_focus: root.input_focus(self.focus)

        Widget:
            id: screen
            #size: self.size
            #pos: self.pos
            #size_hint_y: 1

            canvas:
                Color:
                    rgba: 1, 1, 1, 1  # This color mixes with the image, somehow...

                Rectangle: # background image
                    source: './fluffy-clouds.jpg'
                    size: self.size
                    pos: self.pos

                Color:
                    rgb: 0.5, 0.2, 0  # this is used as the default color for later objects

                Rectangle:  # floor
                    pos: 0, 0
                    size: self.size[0], floor_size_y

                Color:
                    rgba: 0.4, 0.2, 0, 1

                Rectangle:
                    pos: self.size[0] * 0.2 - (col_size_x / 2), floor_size_y
                    size: col_size_x, self.size[1] * 0.5
                Rectangle:
                    pos: self.size[0] * 0.5 - (col_size_x / 2), floor_size_y
                    size: col_size_x, self.size[1] * 0.5
                Rectangle:
                    pos: self.size[0] * 0.8 - (col_size_x / 2), floor_size_y
                    size: col_size_x, self.size[1] * 0.5

    Disk:
        id: disk1
        canvas:
            Color:
                rgb: 0.9, 0.9, 0.2
            Rectangle:
                pos: self.pos
                size: self.size
    Disk:
        id: disk2
        canvas:
            Color:
                rgb: 1.0, 0.2, 0.3
            Rectangle:
                pos: self.pos
                size: self.size
    Disk:
        id: disk3
        canvas:
            Color:
                rgb: 0.2, 0.1, 1.0
            Rectangle:
                pos: self.pos
                size: self.size
    Disk:
        id: disk4
        canvas:
            Color:
                rgb: 0.4, 0.8, 0.1
            Rectangle:
                pos: self.pos
                size: self.size
    Disk:
        id: disk5
        canvas:
            Color:
                rgb: 0.3, 0.7, 0.6
            Rectangle:
                pos: self.pos
                size: self.size
    Disk:
        id: disk6
        canvas:
            Color:
                rgb: 0.9, 0.0, 0.0
            Rectangle:
                pos: self.pos
                size: self.size
    Disk:
        id: disk7
        canvas:
            Color:
                rgb: 0.6, 0.0, 0.4
            Rectangle:
                pos: self.pos
                size: self.size
'''

if __name__ == '__main__':
    main()

