# from servo import *
# from picamera2 import Picamera2, Preview
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
        # print(len(contours))
        # draw in blue the contours that were founded
        cv2.drawContours(output, contours, -1, -1, 150)

        # find the biggest countour (c) by the area
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        print(x + w/2, y + h/2)
        return x+w/2, y+h/2

        ###########################################
        # RETURN COORDINATES IN PRINT STATEMENT!! #
        ###########################################

        # draw the biggest contour (c) in green
        #cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # show the images

    #cv2.imshow("Result", np.hstack([image, output]))

    #cv2.waitKey(0)



def find_distance(filename):
    a,b = find_laser(filename)
    d = 40017 * pow(b, -1.376)

    ######################################
    # Bounds to find off-center distance #
    ######################################
    fL10 = lambda x: -0.11 * x * x + 12.86 * x - 164.4
    fL5 = lambda x: -0.0864 * x * x + 9.3043 * x + 16.8
    fCenter = lambda x: 314
    fR5 = lambda x: 0.0764 * x * x - 8.3843 * x + 603.4
    fR10 = lambda x: 0.1064 * x * x - 12.784 * x + 811.9

    if a < fL10(d):
        #TODO: Fix this for linearization
        print("Greater than L10")
        return d, -10
    elif a < fL5(d):
        print("Between 10 and 5 L")
        k = a - fL10(d)
        j = fL5(d) - a
        return d, (-10)*(k / (k+j)) + (-5)*(j / (k+j))
    elif a < fCenter(d):

        print("Between 5 and 0 L")
        k = a - fL5(d)
        j = fCenter(d) - a
        return d, (-5) * (k / (k + j)) + (0) * (j / (k + j))
    elif a < fR5(d):

        print("Between 0 and 5 R")
        k = a - fR5(d)
        j = fCenter(d) - a
        return d, (0) * (k / (k + j)) + (5) * (j / (k + j))

    elif a < fR10(d):
        print("Between 5 and 10 R")
        k = a - fR10(d)
        j = fR5(d) - a
        return d, (5) * (k / (k + j)) + (10) * (j / (k + j))
    else:
        # TODO: Fix this for linearization
        print("Greater than R10")
        return d, 10






def main():
    

    image_list = []
    for filename in os.listdir("./CalibrationCaptures"):
        ext = filename.split('.')[1].lower()
        if ext == 'jpg' or ext == 'jpeg' or ext == 'png':
            image_list.append("CalibrationCaptures/" + filename)
    for file in image_list:
        find_laser(file)

    # laser_calibration()

    # find_laser("CalibrationCaptures/RedLaser20CM10L.jpg")
    
  
if __name__ == "__main__":
    main()