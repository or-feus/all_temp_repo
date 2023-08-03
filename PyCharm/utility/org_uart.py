import os
import sys
import time
from typing import List

from serial import Serial
from sysv_ipc import SharedMemory, IPC_CREAT

can_dir = "/home/user/jetson-inference/dbict/control/canerr"
lmb_dir = "/home/user/jetson-inference/dbict/control/lmberr"


def open_serial(device, baud_rate=115200, timeout=1):
    ser = Serial(device, baudrate=baud_rate, timeout=timeout)
    if not ser.isOpen():
        ser.open()
    return ser


def hex_dump(message: str, buf: bytearray):
    """
    bytearray 타입의 통신 데이터를 hex로 변환 후 결과를 출력한다.
    ============================================================
    :param message: 출력할 hex타입의 데이터
    :param buf: 송수신되고 있는 bytearray 타입의 데이터
    :return None
    ============================================================
    """

    for value in buf:
        message += " %02X" % value
    print(message)


def genlrc(msg: List):
    """
    Longitudinal Redundancy Check(LRC); 세로 중복 검사
    참고: https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=deepb1ue&logNo=221189953315
    ============================================================
    :param msg: can 컨트롤러에 write하기 전 오류 검출 코드를 검사할 데이터
    :return: LRC Code
    ============================================================
    """

    lrc = 0
    for value in msg:
        lrc ^= value
    return lrc


class CanSerial:

    def __init__(self, shared_memory: SharedMemory, serial: Serial):
        """
        ============================================================
        :param shared_memory : 공유메모리 초기화
        :param uart: CAN 컨트롤러
        ============================================================
        inactive: 영상검지 프로그램 실행여부 체크
        disable:
        can_conn_fail_count:
        detection_code:
        before_start:
        """

        self.shm = shared_memory
        self.ser = serial
        self.shm_memory = bytearray(self.shm.read())

        self.inactive = 0
        self.disable = 0
        self.can_conn_fail_count = 0
        self.detection_code = 0
        self.detection_start = False

        self.shm.write(bytes(64))

        self.next_count = 0

    def receive_uart_msg(self):

        rx_count = self.ser.inWaiting()

        if rx_count < 3:
            return None
        rx_message = self.ser.read(3)

        if rx_message[0] != 0x7e or rx_message[1] != 0x7e:
            time.sleep(0.01)
            rx_count = self.ser.inWaiting()
            rx_message = self.ser.read(rx_count)
            return None

        if rx_count < 71:
            time.sleep(0.01)
            rx_count += self.ser.inWaiting()

        rx_message += self.ser.read(rx_count - 3)
        return rx_message

    def first_start_check(self) -> 0x00 or 0x01 or 0x02:
        check_code = self.detection_code
        if int(self.shm_memory[0]) != 0:
            self.detection_start = True
            self.inactive = 0
            check_code = self.detection_code
        else:
            self.inactive += 1
            if self.inactive >= 50:
                check_code = 0x02

        return check_code

    def running_check(self) -> 0x00 or 0x01 or 0x02:
        check_code = self.detection_code
        if int(self.shm_memory[0]) == self.next_count:
            self.disable += 1
            if self.disable > 100:
                check_code = 0x02
        else:
            self.disable = 0
            check_code = self.detection_code

        if not self.detection_start:
            check_code = 0x02

        return check_code

    def detection_check(self) -> 0x00 or 0x01 or 0x02:

        self.detection_code = (self.shm_memory[1] & 0x0f) | (self.shm_memory[16] << 1)  # detector state
        self.detection_code = self.first_start_check()
        self.detection_code = self.running_check()
        # print((shm_memory[1] & 0x0f) | (shm_memory[16] << 1))
        # return self.detection_code

    def writing(self):
        length = self.shm_memory[42]
        frame_num = 0
        if length > 0:  # server command
            length += 2
            serial_msg = self.shm_memory[40:40 + length]
            self.shm_memory[42] = 0  # clear length
            self.shm.write(self.shm_memory)
        else:
            frame_num = (frame_num + 1) & 0x3f

            serial_msg = [0x7e, 0x7e, 6, 1, 0x00, frame_num, self.detection_code]

            serial_msg.append(genlrc(serial_msg))

        self.ser.write(serial_msg)
        # hex_dump("TXD : ", serial_msg)

    def finally_shm_write(self, receive_message):
        rx_count = len(receive_message)
        if rx_count >= 71 and receive_message[6] is 1 and receive_message[6 + 8] is 2:
            self.shm_memory[128:128 + 64] = receive_message[6:6 + 64]
        else:
            self.shm_memory[80:80 + rx_count] = receive_message

        self.shm.write(self.shm_memory)

    def rx_data_check(self, receive_message):

        can_err_dir = os.path.isdir(can_dir)
        lmb_err_dir = os.path.isdir(lmb_dir)

        if receive_message:
            self.can_conn_fail_count = 0

            os.rmdir(lmb_dir) if receive_message[64] != 0 else os.mkdir(lmb_dir)
            if can_err_dir: os.rmdir(can_dir)

            self.finally_shm_write(receive_message)
        else:
            self.can_conn_fail_count += 1
            if self.can_conn_fail_count is 100:
                self.can_conn_fail_count = 999
                if not can_err_dir: os.mkdir(can_dir)
                if not lmb_err_dir: os.mkdir(lmb_dir)


def main():
    c = CanSerial(
        SharedMemory(0x1000, flags=IPC_CREAT, size=256),
        open_serial("/dev/ttyTHS1", 115200, 1)
    )

    while True:
        try:
            c.shm_memory = bytearray(c.shm.read())
            c.detection_check()
            c.next_count = int(c.shm_memory[0])
            c.writing()
            c.rx_data_check(c.receive_uart_msg())

            time.sleep(0.1)

        except Exception as e:
            print("Except : ", e)
            time.sleep(10)
            sys.exit()


if __name__ == '__main__':
    main()
