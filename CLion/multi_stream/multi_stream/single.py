import cv2

cap = cv2.VideoCapture("http://192.168.1.23:3000/api/get_stream")

while True:
    ret, frame = cap.read()

    if ret == True:
        cv2.imshow('result', frame)

        if cv2.waitKey(10) == ord('q'):
            break


