import cv2

cam = cv2.VideoCapture(cv2.CAP_PROP_SERIAL_NUM)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
while True:
    ret_val, img = cam.read()  # 캠 이미지 불러오기

    cv2.imshow("Cam Viewer", img)  # 불러온 이미지 출력하기
    if cv2.waitKey(1) == 27:
        break  # esc to quit
