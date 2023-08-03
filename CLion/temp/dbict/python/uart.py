import serial
import time
import sysv_ipc
import sys
import datetime
import os


class CAN_Serial:
    def __init__(self, shm, ser, inactive, chk, ser_fail, err, lmb_active, before_start):

        self.shm = shm
        self.ser = ser
        self.inactive = inactive
        self.chk = chk
        self.ser_fail = ser_fail
        self.err = err
        self.lmb_active = lmb_active
        self.before_start = before_start

    def hex_dump(self, msg, buf):
        for value in buf: msg += " %02X" % value
        print(msg)

    def genlrc(self, msg):
        lrc = 0
        for value in msg: lrc ^= value
        return lrc

    def receive_uart_msg(self):
        rxcnt = self.ser.inWaiting()
        if rxcnt < 3: return None
        rxmsg = self.ser.read(3)

        if rxmsg[0] != 0x7e or rxmsg[1] != 0x7e:
            time.sleep(0.01)
            rxcnt = self.ser.inWaiting()
            rxmsg = self.ser.read(rxcnt)
            return None

        if rxcnt < 71:
            time.sleep(0.01)
            rxcnt += self.ser.inWaiting()

        rxmsg += self.ser.read(rxcnt - 3)
        return rxmsg

    def program_chk(self, memory, next_cnt):

        code = (memory[1] & 0x0f) | (memory[16] << 1)  # detector state

        prev_cnt = int(memory[0])

        """
        처음 감응 프로그램 시작 시 self.before_start = False 로 설정 해야 부팅 시 CAN 컨트롤러에 에러코드를 내보낼 수 있다.
        부팅 할 때 에러코드를 CAN에 주지않으면 CAN이 Nano를 재부팅해주지 않는다.
        """
        if memory[0] != 0:  # active-check detectnet
            self.before_start = False
            self.inactive = 0
            self.err = code
        else:  # inactive detectnet
            self.inactive += 1
            if self.inactive >= 50:
                self.inactive = 99
                code = 0x02
                self.err = code
                return self.err

        if prev_cnt == next_cnt:  # error check when detectnet restart
            self.chk += 1

            """ 
            1. 프로그램 종료 후 재시작 하기 까지 1초 ~50초 간 감응 신호 전달
            2. 50초 가 지났을 때 에러코드 전달
            """
            if 10 < self.chk < 500:
                self.err = code = 0x01
                return self.err


            elif self.chk > 500:
                self.err = code = 0x02
                return self.err
            else:
                self.err = code
        else:
            self.chk = 0
            self.err = code

        if self.before_start:
            code = 0x02
            self.err = code
        return self.err

    def write_shm(self, memory):
        length = memory[42]
        frame_num = 0
        if length > 0:  # server command
            length += 2
            sndmsg = memory[40:40 + length]

            memory[42] = 0  # clear length
            # print("write memory : ", memory)
            self.shm.write(memory)

        else:
            frame_num = (frame_num + 1) & 0x3f

            sndmsg = [0x7e, 0x7e, 6, 1, 0x00, frame_num, chkcode]
            # print("length = 0, write memory :", memory)
            sndmsg.append(uart.genlrc(sndmsg))

        # send to UART (CAN_Controller)

        # print("sndmsg : ", sndmsg)
        self.ser.write(sndmsg)
        # uart.hex_dump("TXD : ", sndmsg)

    """
    CAN 컨트롤러와의 통신에 에러가 있는지 확인하기

    물리적인 기본 구성도
    Nano -> CAN -> LMB -> 제어기 CPU 

    현재 버전에서는 CAN에서 받는 데이터(rsvmsg)에서 64번 째(rsvmsg[64])가 0이 아닌 값이 나오게 되었을 때,
    LMB까지 통신이 되는 것으로 간주한다.

    """

    def chk_can_err(self, rcvmsg):

        can_err_dir = os.path.isdir("/home/user/jetson-inference/dbict/control/canerr")
        lmb_err_dir = os.path.isdir("/home/user/jetson-inference/dbict/control/lmberr")
        
        
        if rcvmsg:
            self.ser_fail = 0
            rxcnt = len(rcvmsg)
            if rcvmsg[64] != 0:
                self.lmb_active = True
                if lmb_err_dir:
                    os.rmdir("/home/user/jetson-inference/dbict/control/lmberr")
                else:
                    pass

            else:
                self.lmb_active = False
                if lmb_err_dir == False:
                    os.mkdir("/home/user/jetson-inference/dbict/control/lmberr")
                else:
                    pass

            if can_err_dir:
                os.rmdir("/home/user/jetson-inference/dbict/control/canerr")
            else:
                pass

            if rxcnt >= 71 and rcvmsg[6] == 1 and rcvmsg[6 + 8] == 2:
                memory[128:128 + 64] = rcvmsg[6:6 + 64]
            else:
                memory[80:80 + rxcnt] = rcvmsg
    #        print(memory)
            shm.write(memory)
        else:
            self.ser_fail += 1
            if self.ser_fail > 100:
                self.ser_fail = 999
                if can_err_dir == False:
                    os.mkdir("/home/user/jetson-inference/dbict/control/canerr")
                else:
                    pass
                if lmb_err_dir == False:
                    os.mkdir("/home/user/jetson-inference/dbict/control/lmberr")
                else:
                    pass


inactive = 0
next_cnt = 0
chk = 0
ser_fail = 0
err = False
lmb_active = False
before_start = True
ser = serial.Serial("/dev/ttyTHS1", baudrate=115200, timeout=1)
if ser.isOpen() == False:
    ser.open()

shm = sysv_ipc.SharedMemory(0x1000, flags=sysv_ipc.IPC_CREAT, size=256)
uart = CAN_Serial(shm, ser, inactive, chk, ser_fail, err, lmb_active, before_start)

"""
첫 시작 시 Shared Memory 초기화
"""

memory = bytearray(shm.read())
memory = bytes(64)
shm.write(memory)


while True:
    try:
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')


        memory = bytearray(shm.read())
        chkcode = uart.program_chk(memory, next_cnt)  ## Error check
        next_cnt = int(memory[0])  ## Error check
        #print(chkcode)
        uart.write_shm(memory)  ## Write Shared Memory

        rcvmsg = uart.receive_uart_msg()
        uart.chk_can_err(rcvmsg)


        time.sleep(0.1)


    except Exception as e:
        print("Except : ", e)
        time.sleep(10)
        sys.exit()

