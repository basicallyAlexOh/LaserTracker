import threading
from tracker import Tracker
from distancefinder import DistanceFinder
from motorcontrol import MotorControl
from motorlogger import MotorLogger
from retracer import Retracer
from servo import Servo
from Motor import Motor
import time
import logging


# Runner class: initializes and runs threads for tracker, distancfinder, 
# motorcontrol, motorlogger, and retracer classes
class Runner(object):
    # Declare Static Variables Here
    # lSpeed and rSpeed are integers that set motor control
    lSpeed = 0
    rSpeed = 0
    # laserPos provides an x and y coordinate of the laser from the camera frame
    laserPos = (-1,-1) # 480 x 640 (h, w)
    # relPos provides x and y coordinates of the robots relative position from the laser
    relPos = (-1,-1) # Dist (d, x) from robot
    # array that logs motor controls 
    log = [] # format: (time, lspeed, rspeed)
    motor = Motor()
    initialPath = True

    # lock1, lock2, and condVar are used manage shared data between 
    # tracker, distancefinder, motorcontrol, and motorlogger classes
    lock1 = threading.RLock()
    lock2 = threading.RLock()
    condVar = threading.Condition(lock1)
    pointReady = False



    # position servos head camera into specific orientation
    def __init__(self):
        self.servo = Servo()
        self.servo.setServoPwm('0', 90)
        self.servo.setServoPwm('1', 10)
        print("Created Runner: Waiting 3 seconds...")
        time.sleep(3)
        




    # initializes and runs threads of the classes relevant for tracking laser
    def run(self):
        trackingThread = Tracker()
        distanceThread = DistanceFinder()
        controlThread = MotorControl()
        loggingThread = MotorLogger()

        trackingThread.start()
        distanceThread.start()
        controlThread.start()
        loggingThread.start()

        trackingThread.join()
        distanceThread.join()
        controlThread.join()
        loggingThread.join()


        retracerThread = Retracer()
        retracerThread.start()

        retracerThread.join()
















