import time

import serial

ser = serial.Serial("/dev/ttyUSB0", baudrate=38400, timeout=1)

if not ser.isOpen():
    ser.open()


def gen_lrc(msg):
    lrc = 0
    for value in msg: lrc ^= value
    return lrc


while True:
    length = 0x02
    det_code = 0x01  ## TEMP
    data_code = [length, det_code]
    arr = [0x7E, 0x7E, length, data_code, gen_lrc(data_code)]

    print(arr)
    time.sleep(1)
