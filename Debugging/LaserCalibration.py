from servo import *
from picamera2 import Picamera2, Preview
import cv2


def laser_calibration():
    pwm=Servo()
    pwm.setServoPwm('0',90)
    pwm.setServoPwm('1',0)
    picam2 = Picamera2()
    camera_config = picam2.create_preview_configuration()
    picam2.configure(camera_config)
    picam2.start()
    time.sleep(5)
    picam2.capture_file("imageL.jpg")




def main():
    laser_calibration()
    
  
if __name__ == "__main__":
    main()