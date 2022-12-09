import threading
import runner
import time
import logging

# Retracer class uses motor logs to retrace path taken by following laser ptr 
class Retracer(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        print("Created Retracer")

        i = 0
        self.compressedLog = []
        
        '''
        print("Initial List:")
        for item in runner.Runner.log:
            print(item)
        
        '''
        # compression algorithm to reduce number of motor controls in motor logs to increase retracing precision
        while i < len(runner.Runner.log):
            j = i
            start = runner.Runner.log[i][0]
            while j < len(runner.Runner.log) and (runner.Runner.log[i][1] == runner.Runner.log[j][1] and runner.Runner.log[i][2] == runner.Runner.log[j][2]):
                j += 1
            if j == len(runner.Runner.log):
                end = runner.Runner.log[j-1][0] + runner.Runner.log[j-1][0] - runner.Runner.log[j-2][0]
            else:
                end = runner.Runner.log[j][0]
            self.compressedLog.append((end - start, runner.Runner.log[i][1], runner.Runner.log[i][2]))
            i = j
        print("Log Compression Complete")
        '''
        for item in self.compressedLog:
            print(item)
        '''


        time.sleep(10)

    # run loop that sets motor controls from motor logs
    def run(self):


        for item in self.compressedLog:
            self.set_motors(item[1],item[2])
            time.sleep(item[0]/1.15)
        self.set_motors(0,0)

        
    def set_motors(self, l, r):

        runner.Runner.motor.setMotorModel(l,l,r,r)
        
