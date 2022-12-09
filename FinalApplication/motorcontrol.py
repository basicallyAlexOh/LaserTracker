import threading
import runner
import math
import time
import logging

# MotorControl class uses relPos x,y coorndinates to detemine motor controls to follow laser ptr 
class MotorControl(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        print("Created Motor Controller")

    # run loop that continously generates motor controls 
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
            lSpeed = (int)(baseSpeed * (1 + 1.6 * offset))
            rSpeed = (int)(baseSpeed * (1 - 1.6 * offset))

            self.set_motors(lSpeed, rSpeed)
            
            #time.sleep(1) #TODO: REMOVE THIS

            runner.Runner.lock2.release()
            runner.Runner.lock1.release()
            time.sleep(0.02)
        self.set_motors(0,0)

    # converts relPos x,y coordniates to polar form for analysis 
    def to_polar(self, d, x):
        radius = math.sqrt(d*d + x*x)
        theta = math.atan(x/d)
        return radius, theta

    # determines lSpeed and rSpeed based off polar coordinates 
    def set_motors(self, l, r):
        runner.Runner.motor.setMotorModel(l,l,r,r)
        runner.Runner.lSpeed = l
        runner.Runner.rSpeed = r


