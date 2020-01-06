import threading
from threading import Thread
from time import sleep

class Clock(threading.Thread):
    def __init__(self, father):
        Thread.__init__(self)
        self._stop = threading.Event()
        self.father = father
        self.cont = 0
        self.allDone = False

    def run(self):
        while(not self.allDone):
            sleep(0.01)
            self.cont += 1
            self.father.cbClock(self.cont)

    def stop(self):
        self.allDone = True

    def stopped(self):
        return self.allDone