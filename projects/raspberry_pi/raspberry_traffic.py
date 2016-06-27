# python 3

"""Experiment with Rasperry trafic light
<head>
"""

import RPi.GPIO as GPIO
import time

from collections import namedtuple

TrafLite= namedtuple("TrafLite","cr cy cg pr pg")

def main():

    GPIO.setmode(GPIO.BOARD)

    GPIO.setwarnings(False)

    cross1 = TrafLite(8, 10, 12, 16, 18)
    cross2 = TrafLite(3, 5, 7, 11, 13)

    bt1 = 19
    bt2 = 21

    #on_off(19,8)
    #blink()
    #crossing(bt1,cross1)
    
    thread_crossing(bt1,cross1)
    

def thread_crossing(button, lights):
    
    def my_callback(channel):
        print("start")
        traffic_sequence(lights)
        print("end")
    
    GPIO.setup(button, GPIO.IN)

    for pin in lights:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        
    print("push button {}".format(button))

    #initial state
    GPIO.output(lights.cg, GPIO.HIGH)
    GPIO.output(lights.pr, GPIO.HIGH)

    GPIO.add_event_detect(button, GPIO.FALLING, callback=my_callback)
    print("main-thread goes to sleep")
    time.sleep(20)

    print("Finished")

    GPIO.remove_event_detect(button)

    for pin in lights:
        GPIO.output(pin, GPIO.LOW)



    
def crossing(button,lights):
    end_time= time.time()+10
    
    GPIO.setup(button, GPIO.IN)

    for pin in lights:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        
    print("push button {}".format(button))

    #initial state
    GPIO.output(lights.cg, GPIO.HIGH)
    GPIO.output(lights.pr, GPIO.HIGH)
    
    while True:
        time.sleep(0.1)
        state=GPIO.input(button)
        
        if state==1: # not pressed
            pass
        else: # pressed
            traffic_sequence(lights)

            
        
        if time.time()>end_time:
            break
        
    for pin in lights:
        GPIO.output(pin, GPIO.LOW)

    print("Finished")

def traffic_sequence(lights):
    GPIO.output(lights.cg, GPIO.LOW)
    GPIO.output(lights.cy, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(lights.cy, GPIO.LOW)
    GPIO.output(lights.cr, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(lights.pr, GPIO.LOW)
    GPIO.output(lights.pg, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(lights.pg, GPIO.LOW)
    GPIO.output(lights.pr, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(lights.cr, GPIO.LOW)
    GPIO.output(lights.cg, GPIO.HIGH)
    
def blink():

    channel = 8

    GPIO.setup(channel, GPIO.OUT)

    for _ in range(10):
        GPIO.output(channel, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(channel, GPIO.LOW)
        time.sleep(0.5)

    GPIO.cleanup(channel)

def on_off(button,led):

    end_time= time.time()+10
    
    GPIO.setup(button, GPIO.IN)
    GPIO.setup(led, GPIO.OUT)

    print("push button {}".format(button))
    
    while True:
        time.sleep(0.1)
        state=GPIO.input(button)
        
        if state==1:
            GPIO.output(led, GPIO.LOW)
        else:
            GPIO.output(led, GPIO.HIGH)
        
        if time.time()>end_time:
            break

    print("Finished")
    #print("state:{}".format(str(state)))


    
main()
