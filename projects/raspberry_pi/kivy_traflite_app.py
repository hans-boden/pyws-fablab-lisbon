import time

import time
from queue import Queue

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Ellipse, Color

import rpi_controller
from queue import Queue
from threading import Thread, Event

class G():
    # "hardware" configuration
    red = (1, 0, 0)
    yellow = (0.9, 0.9, 0)
    green = (0, 1, 0)
    coroff = (0.25, 0.25, 0.25)
    xpos = (100, 300)
    ypos = (500, 440, 380, 220, 160)
    cortab = (red, yellow, green, red, green)
    btn_y  = 30

    state1 = 12  # the bits of state (1,2,4,8,16) are for lights (cr, cy, cg, pr, pg)
    state2 = 12
    queue = Queue()
    simgpio = None

    event_pin = 0

def main():
    G.simgpio = SimGPIO(G.queue)
    rpi_controller.setup_controller(G.simgpio)
    app = TrafLiteApp()
    app.run()

class TrafLiteApp(App):
    def build(self):
        simu = TrafficLights()
        return simu

class TrafficLights(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        btn = Button(text="press 10", pos=(G.xpos[0]-15, G.btn_y))
        btn.size = (80,50)
        btn.pin_no = 10
        btn.bind(on_press=self.on_event)
        self.add_widget(btn)

        btn = Button(text="press 20", pos=(G.xpos[1]-15, G.btn_y))
        btn.size = (80, 50)
        btn.pin_no = 20
        btn.bind(on_press=self.on_event)
        self.add_widget(btn)

        Clock.schedule_interval(self.update, 0.05) # 1.0/50.0) 1/50 sec interval

    def on_event(self, obj):
        #print("on event: {}".format(str(obj)))
        G.simgpio.trigger_event(obj.pin_no)

    def update(self, dt):
        if G.state1:
            self.display(G.state1, G.xpos[0])
            G.state1 = 0
        if G.state2:
            self. display(G.state2, G.xpos[1])
            G.state2 = 0

    def display(self, state, xpos):
        d = 50

        with self.canvas:
            for y in range(5):
                bin = 2**(y)
                ypos = G.ypos[y]
                if bin & state:
                    cor = G.cortab[y]
                else:
                    cor = G.coroff

                Color(cor[0], cor[1], cor[2])
                Ellipse(pos=(xpos, ypos), size=(d, d))

class EventThread(Thread):
    def __init__(self, event, callback):
        super().__init__()
        self.event = event
        self.callback = callback # dictionary, key=pin

    def run(self):
        while True:
            rc = self.event.wait(timeout=20)
            if not rc:
                print("event_thread expired")
                break
            # event was triggered
            pin = G.event_pin
            G.event_pin = 0      # reset pin
            self.event.clear()      # reset event
            if pin in self.callback:
                self.callback[pin](pin)  # callback from thread
                
        

class SimGPIO():
    def __init__(self, queue):
        self.queue = queue
        self.state_a = 0
        self.state_b = 0
        self.callback = {}  # callback function for pin number
        self.event = Event()
        self.thread = EventThread(event=self.event, callback=self.callback)
        self.thread.start()  # thread will wait until triggered

    def output(self, pin, state):
        # change the state (on/off) of the output pin
        if pin in (11,12,13,14,15):
            bin = 2**(pin-11)
            if state:
                self.state_a |= bin
            else:
                self.state_a &= 31-bin

        if pin in (21,22,23,24,25):
            bin = 2**(pin-21)
            if state:
                self.state_b |= bin
            else:
                self.state_b &= 31-bin

    def add_event_detect(self, pin, callback):
        # register a callback function
        self.callback[pin] = callback

    def remove_event_detect(self, pin):
        # remove a registered callback function
        if pin in self.callback:
            del self.callback[pin]

    def acknowledge(self):
        # tell the gui to update the traffic light view
        self.queue.put((self.state_a, self.state_b))

    def trigger_event(self, pin):
        print("event detected: {}".format(pin))
        if pin in self.callback:
            if G.event_pin:
                print("overwrite event {}".format(G.event_pin))
            G.event_pin = pin
            self.event.set()

if __name__ == '__main__':
    main()
