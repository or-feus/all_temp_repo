import cv2
import numpy as np

from mjpeg import MjpegServer

cap1 = cv2.VideoCapture("http://59.14.95.196:8888/cam")
cap2 = cv2.VideoCapture("http://59.14.95.196:7777")
cap3 = cv2.VideoCapture("http://59.14.95.196:8888/cam")
cap4 = cv2.VideoCapture("http://59.14.95.196:7080")


@jit
def merge(f1, f2):
    return np.concatenate((f1, f2), axis=1)


def multi_stream(mjpeg_server):
    while True:
        ret1, frame1, = cap1.read()
        ret2, frame2, = cap2.read()
        # ret3, frame3, = cap3.read()
        # ret4, frame4, = cap4.read()
        frame1 = cv2.resize(frame1, dsize=(320, 240))
        frame2 = cv2.resize(frame2, dsize=(320, 240))
        # frame3 = cv2.resize(frame3, dsize=(320, 240))
        # frame4 = cv2.resize(frame4, dsize=(320, 240))
        print("zz")
        if ret1 == True:
            cv2.imshow('result', both1)
            # mjpeg_server.send_img(both1)
            cv2.waitKey(1)
            if cv2.waitKey(10) == ord('q'):
                break


def main():
    mjpeg_server = MjpegServer(port=9999)
    multi_stream(mjpeg_server)


if __name__ == '__main__':
    main()
