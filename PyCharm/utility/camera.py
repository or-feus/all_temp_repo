import cv2
import numpy as np

cap1 = cv2.VideoCapture("http://59.14.95.196:8888/cam")
cap2 = cv2.VideoCapture("http://59.14.95.196:7080")
cap3 = cv2.VideoCapture("http://61.211.241.239/nphMotionJpeg?Resolution=320x240&Quality=Standard")
cap4 = cv2.VideoCapture("http://59.14.95.196:7777")


while True:
    ret1, frame1, = cap1.read()
    ret2, frame2, = cap2.read()
    ret3, frame3, = cap3.read()
    ret4, frame4, = cap4.read()
    frame1 = cv2.resize(frame1, dsize=(320, 240))
    frame2 = cv2.resize(frame2, dsize=(320, 240))
    frame3 = cv2.resize(frame3, dsize=(320, 240))
    frame4 = cv2.resize(frame4, dsize=(320, 240))

    if ret1 == True:
        both1 = np.concatenate((frame1, frame2), axis=1)
        both2 = np.concatenate((frame3, frame4), axis=1)
        both3 = np.concatenate((both1, both2), axis=0)

        cv2.imshow('result', both3)
        cv2.waitKey(200)
        if cv2.waitKey(10) == ord('q'):
            break



