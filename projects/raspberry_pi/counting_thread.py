# python3
"""
    Experiment with python threads
"""

from threading import Thread, Lock
import time

class G():
    counter = 0
    lock = Lock()
    plock = Lock()
    
def main():
    threaded_counter(count_up)
    #threaded_counter(p_count_up)

def threaded_counter(func):
    G.counter = 0
    thread_1 = Thread(target=func, args=(2500000,))
    thread_2 = Thread(target=func, args=(2500000,))
    start = time.time()
    thread_1.start()
    thread_2.start()
    
    pprint("waiting")
    thread_1.join()
    thread_2.join()
    total = time.time()-start
    pprint("time: {:1.2f}".format(total))
    pprint("counter: {}".format(G.counter))

def count_up(number):
    pprint("started thread")
    for _ in range(number):
        G.counter += 1

        
def p_count_up(number):
    pprint("started thread")
    for _ in range(number):
        G.lock.acquire()
        G.counter += 1
        G.lock.release()

def pprint(text):
    G.plock.acquire()
    print(text)
    G.plock.release()

pprint = print
    
        
main()

    
