import threading
import cv2
import numpy as np
from runner import Runner

class Tracker(threading.Thread):


    def __init__(self,group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        print("Created Laser Tracker")

    def run(self):
        with Runner.condVar:
            Runner.lock1.acquire()
            x,y = self.find_laser()
            Runner.laserPos = (x,y)
            pointReady = True
            Runner.condVar.notify()
            Runner.lock1.release()



    def find_laser(self):
        filename = "CalibrationCaptures/tempRedLaser.jpg"
        Runner.camera.capture_file(filename)
        image = cv2.imread(filename)

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

            print(x + w / 2, y + h / 2)
            return x + w / 2, y + h / 2

            # draw the biggest contour (c) in green
            # cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # show the images

        # cv2.imshow("Result", np.hstack([image, output]))

        # cv2.waitKey(0)
        return -1, -1