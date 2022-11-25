import threading
import Tracker
import DistanceFinder
import MotorControl
import MotorLogger
import queue
from picamera2 import Picamera2, Preview
from servo import Servo
from Motor import Motor
import time



class Runner(object):
    # Declare Static Variables Here
    lSpeed = 0
    rSpeed = 0
    laserPos = (-1,-1) # 480 x 640 (h, w)
    relPos = (-1,-1) # Dist (d, x) from robot
    log = [] # format: (time, lspeed, rspeed)
    motor = Motor()
    initialPath = True


    lock1 = threading.RLock()
    lock2 = threading.RLock()
    condVar = threading.Condition(lock1)
    pointReady = False
    camera = Picamera2()
    camera.start()


    def __init__(self):
        self.servo = Servo()
        self.servo.setServoPwm('0', 85)
        self.servo.setServoPwm('1', 0)





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















