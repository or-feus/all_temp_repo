import time

import device
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import threading


#class DEVICE_USBCAM_LIST(threading.Thread, QObject):
class DEVICE_USBCAM_LIST(QThread):
    USBCAM_DEVICE_LIST = pyqtSignal(list)
    def __init__(self):
        QThread.__init__(self)
        self.device_init_flag = True
        self.device_list = []
        self.sleep_time = 2
        self.working =True
    def run(self):
        while self.working :
            if self.exit == True: break
            self.device_list = device.getDeviceList()
            self.USBCAM_DEVICE_LIST.emit(self.device_list)
            self.sleep(self.sleep_time)

    def stop(self):
        self.working = False
        self.quit()
        print("GET_DEVICE END!")
        self.wait(3000)  # 5000ms = 5s

    def __del__(self):
        self.quit()
        self.wait()
        self.device_init_flag = False