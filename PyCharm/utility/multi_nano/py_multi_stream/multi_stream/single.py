import cv2

from mjpeg import MjpegServer

cap = cv2.VideoCapture("http://admin:dongbuict0@59.14.95.196:8888/cam")


def multi_stream(mjpeg_server):
    while True:
        ret, frame = cap.read()
        frame = ~frame
        if ret == True:
            cv2.imshow('result', frame)
            mjpeg_server.send_img(frame)

            if cv2.waitKey(10) == ord('q'):
                break


def main():
    mjpeg_server = MjpegServer(port=9999)
    multi_stream(mjpeg_server)


if __name__ == '__main__':
    main()
