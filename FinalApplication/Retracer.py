import threading
from runner import Runner
import time


class Retracer(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        print("Created Retracer")

    def run(self):
        for i in range(0, len(Runner.log) - 1):
            t1, lSpeed, rSpeed = Runner.log[i]
            t2 = Runner.log[i][0]
            self.set_motors(lSpeed, rSpeed)
            time.sleep(t2-t1)

    def set_motors(self, l, r):
        Runner.motor.setMotorModel(l,l,r,r)
