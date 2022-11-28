import threading
import runner
import math
import time
import logging


class MotorControl(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        print("Created Motor Controller")

    def run(self):
        while runner.Runner.initialPath:
            runner.Runner.lock1.acquire()
            runner.Runner.lock2.acquire()
            
            r, theta = self.to_polar(runner.Runner.relPos[0], runner.Runner.relPos[1])

            baseSpeed = 0
            if r < 10:
                baseSpeed = 0
            elif r < 30:
                baseSpeed = (int) (50 * (r-10))
            else:
                baseSpeed = 1000

            #TODO: Potentially Change to a Polynomial Function for motor offsets
            offset = 2 * math.atan(theta)  # returns value on range [-1,1]
            lSpeed = (int)(baseSpeed * (1 + 1.75 * offset))
            rSpeed = (int)(baseSpeed * (1 - 1.75 * offset))

            self.set_motors(lSpeed, rSpeed)
            
            #time.sleep(1) #TODO: REMOVE THIS

            runner.Runner.lock2.release()
            runner.Runner.lock1.release()
            time.sleep(0.02)
        self.set_motors(0,0)

    def to_polar(self, d, x):
        radius = math.sqrt(d*d + x*x)
        theta = math.atan(x/d)
        return radius, theta

    def set_motors(self, l, r):
        runner.Runner.motor.setMotorModel(l,l,r,r)
        runner.Runner.lSpeed = l
        runner.Runner.rSpeed = r


