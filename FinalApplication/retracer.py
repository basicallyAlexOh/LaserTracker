import threading
import runner
import time
import logging


class Retracer(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        print("Created Retracer")
        time.sleep(10)

    def run(self):
        '''
        for i in reversed(range(0, len(runner.Runner.log) - 1)):
            t1, lSpeed, rSpeed = runner.Runner.log[i+1]
            t2 = runner.Runner.log[i][0]
            lspeed = -1 * lspeed
            rspeed = -1 * rspeed
            #print("From Log: ", (t1-t2)/1000000000, lSpeed, rSpeed)
            self.set_motors(lSpeed, rSpeed)
            time.sleep((t1-t2)/1000000000)
        self.set_motors(0,0)

        '''
        
        for i in range(0, len(runner.Runner.log) - 1):
            t1, lSpeed, rSpeed = runner.Runner.log[i]
            t2 = runner.Runner.log[i+1][0]
            #print("From Log: ", (t2-t1)/1000000000, lSpeed, rSpeed)
            self.set_motors(lSpeed, rSpeed)
            time.sleep((t2-t1)/100)
            
        self.set_motors(0,0)
        
        
    def set_motors(self, l, r):

        runner.Runner.motor.setMotorModel(l,l,r,r)
        
