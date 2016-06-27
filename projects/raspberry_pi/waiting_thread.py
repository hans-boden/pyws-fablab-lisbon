# python3
"""
    Experiment with python threads
"""

from threading import Thread, Lock, Event
import time, random

class G():
    counter = 0
    event_1 = Event()
    event_3 = Event()
    lock = Lock()
    plock = Lock()
    
def main():
    thread_1 = WaitingThread("Zupf", event=G.event_1)
    thread_2 = WaitingThread("Peng", event=G.event_1)
    thread_1.start()
    thread_2.start()

    for _ in range(5):
        pprint("set event 1")
        G.event_1.set()
        time.sleep(2)


    thread_1.join()
    thread_2.join()
    
    thread_3 = WaitingThread("Lala", event=G.event_3)
    thread_3.start()

    for _ in range(5):
        pprint("set event 3")
        G.event_3.set()
        time.sleep(2)

    thread_3.join()


class WaitingThread(Thread):
    def __init__(self, myid, event):
        super().__init__()
        self.myid = myid
        self.event = event
        self.active_count = 0

    def run(self):
        pprint("start Thread {}".format(self.myid))
        while True:
            pprint("{} is waiting".format(self.myid))
            rc = self.event.wait(timeout=5)
            if not rc:
                pprint("{} expired".format(self.myid))
                break
            self.event.clear()
            self.active_count += 1
            pprint("{} is active ({})".format(self.myid, self.active_count))
            time.sleep(random.random()*4)

            
def pprint(text):
    G.plock.acquire()
    print(text)
    G.plock.release()

#pprint = print
    
        
main()

    
