import numpy as np
import cv2


def resize(img):
    return cv2.resize(img, (512, 512))  # arg1- input image, arg- output_width, output_height

# 'D:\WIndows\Music\youtube-dl\Video\Red Dot Video for Cats (10 hours).mkv'
cap=cv2.VideoCapture(0)


ret,frame=cap.read()
l_b=np.array([0,230,170])# lower hsv bound for red
u_b=np.array([255,255,220])# upper hsv bound to red

while ret==True:
    ret,frame=cap.read()
    
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,l_b,u_b)

    contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    '''
    approx=cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True)
    x,y,w,h=cv2.boundingRect(approx)
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),4)
    '''
    
    if len(contours) > 0 :
        max_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(max_contour)
        if M["m00"] !=0 :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            print("CX : "+str(cx)+"  CY : "+str(cy))
            if cx >= 120 :
                print("Turn Left")
                # turn motors left 
            if cx < 120 and cx > 40 :
                print("On Track!")
                # keep motors in same orientation
            if cx <=40 :
                print("Turn Right")
                # turn motors right 
            cv2.circle(frame, (cx,cy), 5, (255,255,255), -1)
    else :
        print("I don't see the line")
        # stop motors 
    
    
    cv2.imshow("frame", resize(frame))

    cv2.imshow("mask", mask)

    key = cv2.waitKey(1)
    if key == ord('q'):
        # turn off motors here 
        break

cv2.waitKey(0)
cv2.destroyAllWindows()




