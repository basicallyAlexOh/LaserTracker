import threading
import runner
import time
import logging

class MotorLogger(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        print("Created MotorLogger")


    def run(self):
        while runner.Runner.initialPath:
            runner.Runner.lock2.acquire()
            runner.Runner.log.append((time.time_ns(), runner.Runner.lSpeed, runner.Runner.rSpeed))
            print("Motor Speeds: ", runner.Runner.lSpeed, runner.Runner.rSpeed)
            #time.sleep(1) #TODO: REMOVE THIS
            runner.Runner.lock2.release()
            time.sleep(0.01)