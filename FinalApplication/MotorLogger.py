import threading
from runner import Runner
import time

class MotorLogger(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        print("Created MotorLogger")


    def run(self):
        Runner.lock2.acquire()
        Runner.log.append((time.time(), Runner.lSpeed, Runner.rSpeed))
        Runner.lock2.release()