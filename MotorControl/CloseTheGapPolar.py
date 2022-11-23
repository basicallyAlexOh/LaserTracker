import time
import math
from Motor import *
from PCA9685 import PCA9685

class CloseTheGap:

    def to_polar(self, X,Y):
        radius = math.sqrt(X*X + Y*Y)
        theta = math.atan(Y/X)
        theta = 180 * theta/math.period

        return radius, theta

    def run_motor(self, X, Y):
        radius, theta = to_polar(X,Y)

        delay1 = 0.1
        radThresh = 30

        # don't do anything if close to center 
        if (radius < 10):
            self.PWM.setXYSpeed(0,0)
            time.sleep(delay1)

        else: 
            # Q2 instructions (right side)
            if (theta<22.5):
                if (radius > radThresh):
                    self.PWM.setXYSpeed(8,2)
                    time.sleep(delay1)
                else:
                    self.PWM.setXYSpeed(4,1)
                    time.sleep(delay1)    
            elif (theta>=22.5 and theta<45):
                if (radius > radThresh):
                    self.PWM.setXYSpeed(8,4)
                    time.sleep(delay1)
                else:
                    self.PWM.setXYSpeed(4,2)
                    time.sleep(delay1)
            elif (theta>=45 and theta<67.5):
                if (radius > radThresh):
                    self.PWM.setXYSpeed(8,6)
                    time.sleep(delay1)
                else:
                    self.PWM.setXYSpeed(4,3)
                    time.sleep(delay1)
            elif (theta>=67.5 and theta<90):
                if (radius > radThresh):
                    self.PWM.setXYSpeed(8,7)
                    time.sleep(delay1)
                else:
                    self.PWM.setXYSpeed(4,3.5)
                    time.sleep(delay1)

            # Q1 instructions (left side)
            elif (theta>=90 and theta<112.5):
                if (radius > radThresh):
                    self.PWM.setXYSpeed(7,8)
                    time.sleep(delay1)
                else:
                    self.PWM.setXYSpeed(3.5,4)
                    time.sleep(delay1)
            elif (theta>=112.5 and theta<135):
                if (radius > radThresh):
                    self.PWM.setXYSpeed(6,8)
                    time.sleep(delay1)
                else:
                    self.PWM.setXYSpeed(3,4)
                    time.sleep(delay1)
            elif (theta>=135 and theta<157.5):
                if (radius > radThresh):
                    self.PWM.setXYSpeed(4,8)
                    time.sleep(delay1)
                else:
                    self.PWM.setXYSpeed(2,4)
                    time.sleep(delay1)
            # elif (theta>=157.5 and theta<180):
            else:
                if (radius > radThresh):
                    self.PWM.setXYSpeed(2,8)
                    time.sleep(delay1)
                else:
                    self.PWM.setXYSpeed(1,4)
                    time.sleep(delay1)



                
