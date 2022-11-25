import threading
from runner import Runner
import math


class MotorControl(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        print("Created Motor Controller")

    def run(self):
        while Runner.initialPath:
            Runner.lock1.acquire()
            Runner.lock2.acquire()
            r, theta = self.to_polar(Runner.relPos[0], Runner.relPos[1])

            baseSpeed = 0
            if r < 10:
                baseSpeed = 0
            elif r < 30:
                baseSpeed = (int) (50 * (r-10))
            else:
                baseSpeed = 1000

            #TODO: Potentially Change to a Polynomial Function for motor offsets
            offset = math.tan(theta / 2)  # returns value on range [-1,1]
            lSpeed = (int)(baseSpeed * (1 + offset))
            rSpeed = (int)(baseSpeed * (1 - offset))

            self.set_motors(lSpeed, rSpeed)

            Runner.lock2.release()
            Runner.lock1.release()

    def to_polar(self, d, x):
        radius = math.sqrt(d*d + x*x)
        theta = math.atan(x/d)
        return radius, theta

    def set_motors(self, l, r):
        Runner.motor.setMotorModel(l,l,r,r)
        Runner.lSpeed = l
        Runner.rSpeed = r


