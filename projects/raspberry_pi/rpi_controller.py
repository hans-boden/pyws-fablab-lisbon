# python3
"""
    learning to program the raspberry pi
    simulate parts of the RPi.GPIO interface
"""
from collections import namedtuple

TrafLite = namedtuple('TrafLite', 'cr cy cg pr pg')

class G():
    btn_a = 10
    lites_a = TrafLite(11, 12, 13, 14, 15)
    btn_b = 20
    lites_b = TrafLite(21, 22, 23, 24, 25)

def setup_controller(simgpio):
    # setup callbacks and initial status
    for pin in G.lites_a:
        simgpio.output(pin, 0)
    for pin in G.lites_b:
        simgpio.output(pin, 0)

    simgpio.output(G.lites_a.cg, 1)
    simgpio.output(G.lites_a.pr, 1)
    simgpio.output(G.lites_b.cg, 1)
    simgpio.output(G.lites_b.pr, 1)

    simgpio.add_event_detect(G.btn_a, handle_btn)
    simgpio.add_event_detect(G.btn_b, handle_btn)

    simgpio.acknowledge() # this is for the GUI simulation only


def handle_btn(pin):
    print("RPiCtl - button {} was pressed".format(pin))

