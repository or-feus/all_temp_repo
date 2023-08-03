import time

import cv2
import numpy as np

from mjpeg import MjpegServer

cap1 = cv2.VideoCapture("http://59.14.95.196:8888/cam")
cap2 = cv2.VideoCapture("http://59.14.95.196:8888/cam")
cap3 = cv2.VideoCapture("http://59.14.95.196:8888/cam")
cap4 = cv2.VideoCapture("http://59.14.95.196:8888/cam")


def merge(f1, f2, align="rows"):
    axis = 1
    if align == "cols":
        axis = 0
    elif align == "rows":
        axis = 1

    return np.concatenate((f1, f2), axis=axis)


def multi_stream(mjpeg_server):
    prev_frame_time = 0
    new_frame_time = 0
    while True:

        new_frame_time = time.time()

        ret1, frame1, = cap1.read()
        ret2, frame2, = cap2.read()
        ret3, frame3, = cap3.read()
        ret4, frame4, = cap4.read()

        frame1 = cv2.resize(frame1, dsize=(320, 240))
        frame2 = cv2.resize(frame2, dsize=(320, 240))
        frame3 = cv2.resize(frame3, dsize=(320, 240))
        frame4 = cv2.resize(frame4, dsize=(320, 240))

        row_1 = merge(frame1, frame2, "rows")
        row_2 = merge(frame3, frame4, "rows")
        result = merge(row_1, row_2, "cols")


        # cv2.imshow('result', result)
        mjpeg_server.send_img(result)
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        print(f"{fps} fps")

        if cv2.waitKey(10) == ord('q'):
            break


def main():
    mjpeg_server = MjpegServer(port=9998)
    multi_stream(mjpeg_server)


if __name__ == '__main__':
    main()
