from servo import *
from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import os

def laser_calibration():
    pwm=Servo()
    pwm.setServoPwm('0',85)
    pwm.setServoPwm('1',0)
    picam2 = Picamera2()
    camera_config = picam2.create_preview_configuration()
    picam2.configure(camera_config)
    picam2.start()
    time.sleep(5)
    picam2.capture_file("CalibrationCaptures/RedLaser40CM10R.jpg")



def find_laser(filename):
    image = cv2.imread(filename)
    print(filename)


    # set blue and green channels to 0
    image[:, :, 0] = 0
    image[:, :, 1] = 0



    for i in range(0, 480):
        for j in range(0, 640):
            if image[i][j][2] < 250:
                image[i][j][2] = 0
    # cv2.waitKey(0)

    # winname = "Test"
    # cv2.namedWindow(winname)  # Create a named window
    # cv2.moveWindow(winname, 40, 30)  # Move it to (40,30)
    # cv2.imshow(winname, r)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    # cv2.waitKey(0)




    # red color boundaries [B, G, R]
    lower = [0, 0, 250]
    upper = [255, 255, 255]

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)

    ret, thresh = cv2.threshold(mask, 100, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:
        print(len(contours))
        # draw in blue the contours that were founded
        cv2.drawContours(output, contours, -1, -1, 150)

        # find the biggest countour (c) by the area
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        print(x + w/2, y + w/2)

        # draw the biggest contour (c) in green
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # show the images

    cv2.imshow("Result", np.hstack([image, output]))

    cv2.waitKey(0)


def main():
    
    '''
    image_list = []
    for filename in os.listdir("./CalibrationCaptures"):
        ext = filename.split('.')[1].lower()
        if ext == 'jpg' or ext == 'jpeg' or ext == 'png':
            image_list.append("CalibrationCaptures/" + filename)
    for file in image_list:
        find_laser(file)
    '''
    laser_calibration()

    # find_laser("CalibrationCaptures/RedLaser20CM10L.jpg")
    
  
if __name__ == "__main__":
    main()