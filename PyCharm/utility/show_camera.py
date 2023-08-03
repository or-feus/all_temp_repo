import cv2

cap = cv2.VideoCapture("/dev/video0")

while (cap.isOpened()):
    ret, frame, = cap.read()

    if ret:
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("image", image)

        if cv2.waitKey(10) == ord('q'):
            break

