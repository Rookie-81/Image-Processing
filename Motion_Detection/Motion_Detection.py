'''


__________                  __    .__           ______   ____
\______   \  ____    ____  |  | __|__|  ____   /  __  \ /_   |
 |       _/ /  _ \  /  _ \ |  |/ /|  |_/ __ \  >      <  |   |
 |    |   \(  <_> )(  <_> )|    < |  |\  ___/ /   --   \ |   |
 |____|_  / \____/  \____/ |__|_ \|__| \___  >\______  / |___|
        \/                      \/         \/        \/


'''

import numpy as np
import cv2 as cv
import time
import datetime
import imutils
import serial

####Parameters###
Min_Area = 1000  # Minimum area of pixels to detect
Movement_Confidence = 0  # time before the program is confident that there is movement

# ==========================================================================================================#
# Main INNIT#
# ==========================================================================================================#
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
font = cv.FONT_HERSHEY_COMPLEX_SMALL
# HISTORY, THRESHOLD , SHADOWS
foreground = cv.createBackgroundSubtractorMOG2(200, 100, detectShadows=True)
motion_flag = 0
ser1 = serial.Serial('COM8',9600)  # set the communication port and set the baude rate to the same rate the arduino is running
# MAIN LOOP!

while True:
    ret, frame = cap.read()
    foremask = foreground.apply(frame)

    contours = cv.findContours(foremask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    for cnt in contours:
        (x, y, w, h) = cv.boundingRect(cnt)
        if cv.contourArea(cnt) > Min_Area:
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            text = "Motion Detected"
            motion_flag = '1'
            print(motion_flag)

            ser1.write(motion_flag.encode())  # Send 1s when motion is detected to the arduino
            cv.putText(frame, str(text), (10, 35), font, 0.75, (255, 255, 255), 1, cv.LINE_AA)
        else:
            pass

    cv.putText(frame, datetime.datetime.now().strftime('%A %d %B %Y %I:%M:%S%p'), (320, 470), cv.FONT_HERSHEY_SIMPLEX,
               0.5, (255, 255, 255), 1)
    # For if you want to show the individual video frames
    # cv.imshow('mask',foremask)
    # cv.imshow("frame", frame)
    foremask = cv.cvtColor(foremask, cv.COLOR_GRAY2BGR)
    cv.imshow("frame", np.hstack((foremask, frame)))

    ch = cv.waitKey(1)
    if ch & 0xFF == ord('q'):
        break

# Cleanup when closed
cv.waitKey(0)
cv.destroyAllWindows()
cap.release()
