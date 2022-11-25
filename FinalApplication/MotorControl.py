import threading
from runner import Runner
import math
from PCA9685 import PCA9685


class MotorControl(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        print("Created Motor Controller")

    def run(self):
        Runner.lock1.acquire()
        Runner.lock2.acquire()
        r, theta = self.to_polar(Runner.relPos[0], Runner.relPos[1])
        if r < 10:
            self.set_motors(0,0)
        else:






        Runner.lock2.release()
        Runner.lock1.release()

    def to_polar(self, d, x):
        radius = math.sqrt(d*d + x*x)
        theta = math.atan(x/d)
        theta = 180 * theta / math.pi
        return radius, theta

    def set_motors(self, l, r):
        Runner.motor.setMotorModel(l,l,r,r)
        Runner.lSpeed = l
        Runner.rSpeed = r


