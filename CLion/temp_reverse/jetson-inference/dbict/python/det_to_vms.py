import serial
import sysv_ipc
import time

ser = serial.Serial("/dev/ttyUSB0", baudrate=38400, timeout=1)
shm = sysv_ipc.SharedMemory(0x1000)
if not ser.isOpen():
    ser.open()


def gen_lrc(msg):
    lrc = 0
    for value in msg: lrc ^= value
    return lrc

while True:

    try:
        shm_memory = bytearray(shm.read())
        length = 0x02
        det_code = 0x00  ## TEMP
        data_code = [length, det_code]

        arr = bytearray(5)

        arr = [0x7E, 0x7E, 0x02, int(shm_memory[0])]
        arr.append(gen_lrc(arr))
        ser.write(arr)
        print(arr)
        time.sleep(0.1)


    except Exception as e:
        print("Except : ", e)
        time.sleep(10)
        sys.exit()
