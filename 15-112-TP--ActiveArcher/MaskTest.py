#################################################
# Term Project - Raj Mehta (rajm)
# Your andrew id: rajm
#################################################

import cv2
import math, copy, random
import numpy as np
from cmu_112_graphics import *

#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################

#Function allows us to pass an empty parameter when tracking Colour
def nothing(x):
    pass

#Allows the user to use adjustable sliders to calibrate their device
#Some of the code in this function was from youtube channel programming knoweldge
#The code from programming Knowledge was used to create slidebars
def getColourTracking():
    #cv2.VideoCapture(0) allows us to access the webcam
    cameraCapture = cv2.VideoCapture(0)
    
    #Creates the window allowing with adjustable sliders
    cv2.namedWindow("Tracking")
    cv2.createTrackbar("LH","Tracking",0,255, nothing)
    cv2.createTrackbar("LS","Tracking",0,255, nothing)
    cv2.createTrackbar("LV","Tracking",0,255, nothing)
    cv2.createTrackbar("UH","Tracking",0,255, nothing)
    cv2.createTrackbar("US","Tracking",0,255, nothing)
    cv2.createTrackbar("UV","Tracking",0,255, nothing)

    
    

    while (True):
        #Allows to get video footage frame by frame
        ret, frame = cameraCapture.read()
        cv2.imshow('frame',frame)

        #Converts each fram to HSV. HSV is a color format, processes image
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        l_h = cv2.getTrackbarPos("LH", "Tracking")
        l_s = cv2.getTrackbarPos("LS", "Tracking")
        l_v = cv2.getTrackbarPos("LV", "Tracking")

        u_h = cv2.getTrackbarPos("UH", "Tracking")
        u_s = cv2.getTrackbarPos("US", "Tracking")
        u_v = cv2.getTrackbarPos("UV", "Tracking")
        
        #Gets a lower and upper bound through the slidebars
        lower_bound = np.array([l_h,l_s,l_v])
        upper_bound = np.array([u_h,u_s,u_v])
        #Bounds are used to create a mask that allows to track only our desired object
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        #Different image windows allow user to see what mask will look like
        cv2.imshow("frame", frame)
        cv2.imshow("mask" , mask)
        cv2.imshow("res", res)
        #Pressing Q breaks us from the loop
        if cv2.waitKey(1) == ord('q'):
            break 

    cameraCapture.release()
    cv2.destroyAllWindows()

    #returns the bounds found through adjusting sliders for the main part of the game
    return [l_h, l_s, l_v, u_h, u_s, u_v]


def captureColor(t):
    cameraCapture = cv2.VideoCapture(0)

    while (True):
        ret, frame1 = cameraCapture.read()
        
        #ret, frame2 = cameraCapture.read()
        #diff = cv2.absdiff(frame1, frame2)

        #Image processesing: Conver to hsv and detects rapid movement
        hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        blur = cv2.GaussianBlur(hsv, (5,5), 0)
        #Same bounds from previous function
        lower_bound = np.array([t[0],t[1],t[2]])
        upper_bound = np.array([t[3],t[4],t[5]])

        #Best known detection values
        #lower_bound = np.array([0,170,102])
        #upper_bound = np.array([255,255,255])

        #Various image processising techniques to analyze desired section
        mask = cv2.inRange(blur, lower_bound, upper_bound)
        mask = cv2.erode(mask, None, iterations=2)
        
        #These sets of lines that identify countours around desired object
        _, thresh = cv2.threshold(mask, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        #Created a list to add the coordinates of the two paddles
        L = [0,0]   
        i = 0
        #Appends contours to list, prevents more than two objects from being detected
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 1000 :
                continue
            if i > 1:
                i = 1
            L[i] = (x,y)
            i += 1
            #Draws shapes around paddles and tells us if we need to reposition them
            cv2.rectangle(frame1, (x,y), (x+w, y+h), (255,0,0), 2)
            cv2.putText(frame1, f'C {x},{y}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
        if L[0] == 0 or L[1]  == 0:
            cv2.putText(frame1, f'Reposition Paddles', (10,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
    
        cv2.imshow("frame", frame1)

        #Convert x,y coordinates of paddles into polar coordiantes
        if type(L[0]) == tuple and type(L[1]) == tuple:
            x1 = L[0][0]
            y1 = L[0][1]
            x2 = L[1][0]
            y2 = L[1][1]
            if abs(x1-x2) < 100 or abs(y1-y2) < 100:
                print('NewArrow')
            rDistance = ((x1-x2)**2-(y1-y2)**2)**0.5
            theta = math.atan((y2-y1)/(x2-x1))
            print(rDistance)
            print(theta)

        if cv2.waitKey(1) == ord('q'):
            break 

    cameraCapture.release()
    cv2.destroyAllWindows()

captureColor(getColourTracking())

