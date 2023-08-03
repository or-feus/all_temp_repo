# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 18:15:41 2021

@author: parkbumjin
"""
import asyncio
import time
from multiprocessing import Process


import sys

import cv2
from PyQt5 import uic, QtCore
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QGraphicsDropShadowEffect, QSizeGrip
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import pyqtSlot, QTimer, QPropertyAnimation, QObject, QIODevice, QByteArray, QWaitCondition, QMutex, \
    Qt
import os
import threading
# CUSTOM FILE
import SOC_ICD
from IMG_PROCESS_TEMP import *
from SOC_CMD import *
from USBCAM_LIST_GET import *


os.system('Pyrcc5 QuantumRED_MAIN.qrc -o QuantumRED_MAIN_rc.py')

form_class = uic.loadUiType("QuantumRED_MAIN_TEMP.ui")[0]

__platform__ = sys.platform

counter = 0
WINDOW_SIZE = 0


class SerialReadThread(QThread):
    # 사용자 정의 시그널 선언
    # 받은 데이터 그대로를 전달 해주기 위해 QByteArray 형태로 전달
    received_data = pyqtSignal(QByteArray, name="receivedData")
    def __init__(self, serial):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self._status = False
        self.mutex = QMutex()
        self.serial = serial
        self.exit = False
        self.working = True

    def __del__(self):
        self.wait()

    def run(self):
        while self.working:
            if self.exit == True: break
            self.mutex.lock()
            if not self._status:
                self.cond.wait(self.mutex)

            buf = self.serial.readAll()
            if buf:
                self.received_data.emit(buf)
            self.usleep(1)
            self.mutex.unlock()

    def stop(self):
        self.working = False
        self.quit()
        print("Serial Thread END!")
        self.wait(2000)

    def toggle_status(self):
        self._status = not self._status
        if self._status:
            self.cond.wakeAll()

    @pyqtSlot(bool, name='setStatus')
    def set_status(self, status):
        self._status = status
        if self._status:
            self.cond.wakeAll()

class QuantumRED_MAIN_TEMP(QMainWindow, form_class, QObject):
    BAUDRATES = (
        QSerialPort.Baud1200,
        QSerialPort.Baud2400,
        QSerialPort.Baud4800,
        QSerialPort.Baud9600,
        QSerialPort.Baud19200,
        QSerialPort.Baud38400,
        QSerialPort.Baud57600,
        QSerialPort.Baud115200,
    )

    DATABITS = (
        QSerialPort.Data5,
        QSerialPort.Data6,
        QSerialPort.Data7,
        QSerialPort.Data8,
    )

    FLOWCONTROL = (
        QSerialPort.NoFlowControl,
        QSerialPort.HardwareControl,
        QSerialPort.SoftwareControl,
    )

    PARITY = (
        QSerialPort.NoParity,
        QSerialPort.EvenParity,
        QSerialPort.OddParity,
        QSerialPort.SpaceParity,
        QSerialPort.MarkParity,
    )

    STOPBITS = (
        QSerialPort.OneStop,
        QSerialPort.OneAndHalfStop,
        QSerialPort.TwoStop,
    )
    received_data = pyqtSignal(QByteArray, name="receivedData")
    received_data2 = pyqtSignal(QByteArray, name="receivedData2")
    sent_data = pyqtSignal(str, name="sentData")

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.auto_check = True
        self.run = False
        self.simul = False
        self.TEC_mouse_ing = False
        self.TARGET_mouse_ing = False

        self.TEC_TEMP_DISPLAY_FLAG = False
        self.TARGET_TEMP_DISPLAY_FLAG = False
        self.EDGE_ACTIVE = True
        self.NF_ACTIVE = True
        self.EZOOM_ACTIVE = True
        self.COLOR_ACTIVE = True
        self.NUC_AUTO = False
        self.CEM_ACTIVE = True

        self.IMG_PROCESS = IMAGE_PROCESS_TEMP()
        #self.DEVICE_GET = DEVICE_USBCAM_LIST()
        self.DEVICE_GET = DEVICE_USBCAM_LIST()
        #self.DEVICE_GET.daemon=True
        self.DEVICE_GET.start()
        self.device_list = []
        self.prev_device_list= []
        self.cnt = 0
        self.target_value_sum = 0
        self.tec_value_sum = 0
        self.cnt_target_avg = 0
        self.cnt_avg = 0
        self.TEMP_DISTANCE_VAL = 3
        # EXTERNAL PYQTSIGNAL
        self.IMG_PROCESS.frame_signal1.connect(self.FRAME_RAW_DISPLAY)
        self.IMG_PROCESS.state_signal.connect(self.state_control)
        self.DEVICE_GET.USBCAM_DEVICE_LIST.connect(self.GET_USB_DEVICE_LIST)
        self.TABLE_MAT = dict()

        # remove title bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.frame_header.mouseMoveEvent = self.MOVE_WINDOW
        # TEMP_AVG_LIST
        self.TEMP_LIST = []
        self.ICD = SOC_ICD.SOC_ICD()
        # SERIAL SET
        self.serial = QSerialPort()
        self.serial_info = QSerialPortInfo()
        self.serial_read_thread = SerialReadThread(self.serial)
        self.serial_read_thread.received_data.connect(lambda v: self.received_data.emit(v))
        self.serial_read_thread.start()

        self.init_widget()
        #deadmap
        self.frame_sum = np.zeros((5,240,320))
        self.target_offset = 0.0

        #self.device_list = self.DEVICE_GET.device_list


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'MSG', "You really want to quit QuantumRed Console?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                if self.IMG_PROCESS.uvc_cap.isOpened():
                    self.IMG_PROCESS.uvc_cap.release()
                    print("Video_close END!")
                else:
                    print("No VIDEO CAP")
            except:
                print("No VIDEO CAP")
            if self.IMG_PROCESS.isRunning():
                self.IMG_PROCESS.stop()
            if self.DEVICE_GET.isRunning():
                self.DEVICE_GET.stop()
            if self.serial_read_thread.isRunning():
                self.serial_read_thread.stop()
            try:
                self.dlg.close()
            except:
                pass
            event.accept()
        else:
            event.ignore()

    def init_widget(self):
        self.sb = self.statusBar()
        self.setStatusBar(self.sb)
        self.image_label.resize(self.IMG_PROCESS.m_nXres, self.IMG_PROCESS.m_nYres)
        self.Play_BTN.clicked.connect(self.VIDEO_PLAY)
        self.START_BTN.clicked.connect(self.START_STOP_FUNC)
        self.SNAPSHOT_BTN.clicked.connect(self.SNAPSHOT)
        self.Video_Save_BTN.clicked.connect(self.VIDEO_SAVE_STOP)
        self.TARGET_OSD_CHK.setChecked(False)
        self.TARGET_OSD_CHK.stateChanged.connect(lambda : self.OSD_ON_OFF("TARGET"))
        self.image_label.mousePressEvent = self.GET_PIXEL_START
        self.image_label.mouseMoveEvent = self.GET_PIXEL_ING
        self.image_label.mouseReleaseEvent = self.GET_PIXEL_END

        # CONTROL BUTTON COMBOBOX / BTN DISABLE
        self.comboBox_EDGE.setEnabled(True)
        self.PB_EDGE.setEnabled(True)
        self.comboBox_NF.setEnabled(True)
        self.PB_NF.setEnabled(True)
        self.CMD_CONTROL_BTN_ON_OFF(False)

        self.TARGET_OSD_TEMP.setText("0.00")
        self.PB_MENU.clicked.connect(self.SLIDE_LEFT_MENU)

        # LEFT MENU BTN
        self.PB_CAMERA.clicked.connect(lambda: self.EVENT_LEFT_MENU_BTN(self.CAMERA_PAGE))
        self.PB_CONTROL.clicked.connect(lambda: self.EVENT_LEFT_MENU_BTN(self.CONTROL_PAGE))
        self.PB_SETTING.clicked.connect(lambda: self.EVENT_LEFT_MENU_BTN(self.SETTING_PAGE))

        # WINDOW BTN MENU
        self.PB_WD_DOWN.clicked.connect(lambda: self.showMinimized())
        self.PB_WD_RESTORE.clicked.connect(lambda: self.RESTORE_MAXIMIZE_WINDOW())
        self.PB_WD_CLOSE.clicked.connect(lambda: self.close())

        # SOC CONTROL BTN
        self.PB_CEM.clicked.connect(lambda: self.LEFT_BTN_ACTIVE("CEM"))
        self.PB_EDGE.clicked.connect(lambda : self.LEFT_BTN_ACTIVE("EDGE"))
        self.PB_NF.clicked.connect(lambda: self.LEFT_BTN_ACTIVE("NF"))
        self.PB_EZOOM.clicked.connect(lambda: self.LEFT_BTN_ACTIVE("EZOOM"))
        self.PB_REF_MOVE.clicked.connect(self.REF_MOVE_SHOW)

        # VIDEO/SNAP DIR SET
        self.PB_SNAP_SAVE_DIR.clicked.connect(lambda: self.GET_DIR_VIDEO_SNAP("SNAP"))
        self.PB_VIDEO_SAVE_DIR.clicked.connect(lambda: self.GET_DIR_VIDEO_SNAP("VIDEO"))
        self.PB_NUC_PERIOD.clicked.connect(self.NUC_AUTO_START)

        # CEM_SELEC
        self.PB_CEM_SET.clicked.connect(self.SET_CEM_TYPE)

        # COMBOBOX COLOR
        self.cb_mode_sel.setStyleSheet(
            "QComboBox{color: rgb(255, 255, 255);}")
        self.cb_UVC_CH.setStyleSheet(
            "QComboBox{color: rgb(255, 255, 255);}")

        self.PB_EZOOM_SET.setStyleSheet(
            "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_DISABLE.png)}")
        self.PB_COLOR_SET.setStyleSheet(
            "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_DISABLE.png)}")
        self.PB_CEM_SET.setStyleSheet(
            "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_DISABLE.png)}")
        self.PB_EDGE_SET.clicked.connect(lambda: self.EDGE_ON_OFF(self.comboBox_EDGE.currentText()))
        self.PB_NF_SET.clicked.connect(lambda: self.NF_ON_OFF(self.comboBox_NF.currentText()))
        self.PB_EZOOM_SET.clicked.connect(lambda: self.EZOOM_ON_OFF(self.comboBox_EZOOM.currentText()))
        self.PB_COLOR_SET.clicked.connect(lambda: self.COLOR_ON_OFF(self.comboBox_COLOR.currentText()))
        self.PB_NUC.clicked.connect(lambda: self.SOC_CMD_SEND("1-REF_NUC"))
        # SERIAL SET
        self.cb_port.insertItems(0, self._get_available_port())
        # self.cb_port.setDuplicatesEnabled(True)
        self.Serialport_pb.clicked.connect(self.SERIAL_PORT_UPDATE)
        self.Connect_pb.clicked.connect(self.slot_clicked_connect_button)
        # TEMP_DISTANCE CAL
        self.PB_DISTANCE.clicked.connect(self.TEMP_DIST_VAL_SET)
        # TEMP GET TYPE
        self.comboBox_TEMP_TYPE.currentTextChanged.connect(self.GET_TEMP_TYPE)
        QSizeGrip(self.frame_SIZE_GRIP)
        self.sb.showMessage('Ready', 10000)
        self.cb_UVC_CH.insertItems(0, self.device_list)
        for idx in range(len(self.device_list)):
            self.cb_UVC_CH.setItemIcon(idx, QIcon(":/ICON/resource/ICON/004-camera.png"))

    # ==================================================================================================================
    # IMG_PROCESS_FUNC
    # ==================================================================================================================
    def EDGE_ON_OFF(self, type):
        self.IMG_PROCESS.EDGE_ON = True
        self.IMG_PROCESS.EDGE_Type = type

    def NF_ON_OFF(self, type):
        self.IMG_PROCESS.NF_ON = True
        self.IMG_PROCESS.NF_Type = type

    def EZOOM_ON_OFF(self, type):
        self.IMG_PROCESS.EZOOM_ON = True
        self.IMG_PROCESS.EZOOM_Type = type

    def COLOR_ON_OFF(self, type):
        self.IMG_PROCESS.COLOR_ON = True
        self.IMG_PROCESS.COLOR_Type = type

    # TEMP_TYPE GET
    def GET_TEMP_TYPE(self):
        self.IMG_PROCESS.GET_TYPE = self.comboBox_TEMP_TYPE.currentText()
        #self.textBrowser.append("TEMP_TYPE = %s", self.IMG_PROCESS.GET_TYPE)
    #CEM SET
    def SET_CEM_TYPE(self):
        cem_type = self.comboBox_CEM.currentText()
        cem_type = cem_type.replace("CEM", "")
        self.IMG_PROCESS.CEM_TYPE = cem_type

    #===================================================================================================================
    # SERIAL_SETTING_FUNC
    #===================================================================================================================
    def SOC_CMD_SEND(self, CMD):
        STX = b'\x02'
        ETX = b'\x03'
        CRC = b'\x00'
        data_dummy = b'\x00\x00\x00\x00\x00\x00'
        ICD = self.ICD.SEND_ICD[CMD]
        cmd_data = STX.__add__(ICD['CONSOLE_SOURCE']).__add__(ICD['CONSOLE_DESTINATION']).__add__(
            ICD['CONSOLE_HEADER']).__add__(ICD['Addr']).__add__(ICD['data']).__add__(data_dummy).__add__(
            CRC).__add__(ETX)
        #print(cmd_data)
        self.SOC_SERIAL_SEND(cmd_data)
        if CMD == "TEC_ON":
            self.TEC_FLAG = "TEC_OFF"
            self.Tec_on_off_pb.setStyleSheet(
                "QPushButton{border-image :url(:/Button/resource/BUTTON/TEC_OFF.png)}"
                "QPushButton:hover{border-image: url(:/Button/resource/BUTTON/TEC_OFF_HOVER.png)}")
        if CMD == "TEC_OFF":
            self.TEC_FLAG = "TEC_ON"
            self.Tec_on_off_pb.setStyleSheet(
                "QPushButton{border-image :url(:/Button/resource/BUTTON/TEC_ON.png)}"
                "QPushButton:hover{border-image: url(:/Button/resource/BUTTON/TEC_ON_HOVER.png)}")
        if CMD == "CEM_ON":
            self.CEM_FLAG = "CEM_OFF"
            self.Cem_on_off_pb.setStyleSheet(
                "QPushButton{border-image :url(:/Button/resource/BUTTON/CEM_OFF.png)}"
                "QPushButton:hover{border-image: url(:/Button/resource/BUTTON/CEM_OFF_HOVER.png)}")
        if CMD == "CEM_OFF":
            self.CEM_FLAG = "CEM_ON"
            self.Cem_on_off_pb.setStyleSheet(
                "QPushButton{border-image :url(:/Button/resource/BUTTON/CEM_ON.png)}"
                "QPushButton:hover{border-image: url(:/Button/resource/BUTTON/CEM_ON_HOVER.png)}")
        if CMD == '1-REF_NUC':
            self.SOC_CMD_SEND('TRSM_REF_APPLY')

        return cmd_data

    def SHUTTER_OPEN(self, test):
        Header = b'\x00'
        start = b'\x02'
        end = b'\x03'
        SRC = b'\x02'
        DST = b'\x03'
        Addr = b'\x61'
        CRC = b'\x00'
        data = b'\x00'
        data_dummy = b'\x00\x00\x00\x00\x00\x00'
        cmd_data = start.__add__(SRC).__add__(DST).__add__(Header).__add__(Addr).__add__(data).__add__(
            data_dummy).__add__(CRC).__add__(end)
        self.SOC_SERIAL_SEND(cmd_data)

        return cmd_data

    def SHUTTER_CLOSE(self, test):
        Header = b'\x00'
        start = b'\x02'
        end = b'\x03'
        SRC = b'\x02'
        DST = b'\x03'
        Addr = b'\x73'
        CRC = b'\x00'
        data = b'\x00'
        data_dummy = b'\x00\x00\x00\x00\x00\x00'

        cmd_data = start.__add__(SRC).__add__(DST).__add__(Header).__add__(Addr).__add__(data).__add__(
            data_dummy).__add__(CRC).__add__(end)

        self.SOC_SERIAL_SEND(cmd_data)
        return cmd_data

    def Timer_start(self):
        self.SOC_CMD_SEND("1-REF_NUC")
        period = self.dsb_NUC_period.value()
        self.timer = threading.Timer(period, self.Timer_start)
        self.timer.start()

    def SERIAL_PORT_UPDATE(self):
        self.cb_port.clear()
        # self.cb_port.addItems(self._get_available_port())
        # self.cb_port.removeItem(0)
        self.cb_port.insertItems(0, self._get_available_port())
        QMessageBox.information(self, "MSG", "PORT UPDATE COMPLETE!")

    @staticmethod
    def get_port_path():
        return {"linux": '/dev/ttyS', "win32": 'COM'}[__platform__]

    def _get_available_port(self):
        available_port = list()
        port_path = self.get_port_path()

        for number in range(150):
            #time.sleep(0.01)
            port_name = port_path + str(number)
            if not self._open(port_name):
                continue
            available_port.append(port_name)
            self.serial.close()
        self.serial_port = available_port
        return available_port

    def _open(self, port_name, baudrate=QSerialPort.Baud9600, data_bits=QSerialPort.Data8,
              flow_control=QSerialPort.NoFlowControl, parity=QSerialPort.NoParity, stop_bits=QSerialPort.OneStop):
        info = QSerialPortInfo(port_name)
        self.serial.setPort(info)
        self.serial.setBaudRate(baudrate)
        self.serial.setDataBits(data_bits)
        self.serial.setFlowControl(flow_control)
        self.serial.setParity(parity)
        self.serial.setStopBits(stop_bits)
        return self.serial.open(QIODevice.ReadWrite)

    def connect_serial(self):
        serial_info = {
            "port_name": self.cb_port.currentText(),
            #"baudrate": self.BAUDRATES[self.cb_baud_rate.currentIndex()],
            "baudrate": QSerialPort.Baud115200,
            "data_bits": QSerialPort.Data8,
            "flow_control": QSerialPort.NoFlowControl,
            "parity": QSerialPort.NoParity,
            "stop_bits": QSerialPort.OneStop,
        }
        status = self._open(**serial_info)
        self.serial_read_thread.setStatus(status)
        return status

    def disconnect_serial(self):
        return self.serial.close()

    # @pyqtSlot(bytes, name="writeData")
    def write_data(self, data):
        self.serial.writeData(data)

    def Send_MSG_Set(self):
        self.send_msg = self.send_lineEdit.text()


    @pyqtSlot(name="clickedConnectButton")
    def slot_clicked_connect_button(self):
        if self.serial.isOpen():
            self.disconnect_serial()
            time.sleep(0.1)
            self.Connect_pb.setStyleSheet(
                "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/CONNECT.png)}"
                "QPushButton:hover{border-image: url(:/BTN/resource/QuantumRED_MAIN/CONNECT_HOVER.png)}"
                "QPushButton:hover{border-image: url(:/BTN/resource/QuantumRED_MAIN/CONNECT_PRESSED.png)}")
            QMessageBox.information(self, "MSG", "Serial Disconnect!")
            # self.dlg.close()
            # self.SOC_BTN_INIT("OFF")
        else:
            self.connect_serial()
            time.sleep(0.1)
            if self.serial.isOpen():
                self.Connect_pb.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/DISCONNECT.png)}"
                    "QPushButton:hover{border-image: url(:/BTN/resource/QuantumRED_MAIN/DISCONNECT_HOVER.png)}"
                    "QPushButton:hover{border-image: url(:/BTN/resource/QuantumRED_MAIN/DISCONNECT_PRESSED.png)}")
                QMessageBox.information(self, "MSG", "Serial Connect Success!")
        self.Connect_pb.setText({False: '', True: ''}[self.serial.isOpen()])

    @pyqtSlot(bytes)
    def SOC_SERIAL_SEND(self, Serial_W_Data):
        self.write_data(Serial_W_Data)


    # ==================================================================================================================
    # UI_SETTING_FUNC
    # ==================================================================================================================
    def EVENT_LEFT_MENU_BTN(self, TYPE_BTN):
        width = self.frame_leftmenu.width()
        if width == 90:
            new_width = 186
            self.animation = QPropertyAnimation(self.frame_leftmenu, b"maximumWidth")
            self.animation.setDuration(250)
            self.animation.setStartValue(90)
            self.animation.setEndValue(new_width)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
            self.label_HANWHA_SYTEMS.setStyleSheet(
                "QLabel{border-image :url(:/ICON/resource/QuantumRED_MAIN/HANWHA_SYTEMS.png);}")
        else:
            pass
        self.stackedWidget_MENU.setCurrentWidget(TYPE_BTN)

    def MOVE_WINDOW(self, e):
        if self.isMaximized() == False:
            if e.buttons() == Qt.LeftButton:
                self.move(self.pos() + e.globalPos() - self.clickPosition)
                self.clickPosition = e.globalPos()
                e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def RESTORE_MAXIMIZE_WINDOW(self):
        global WINDOW_SIZE
        win_state = WINDOW_SIZE
        if win_state == 0:
            WINDOW_SIZE = 1
            self.showMaximized()
        else :
            WINDOW_SIZE = 0
            self.showNormal()

    def SLIDE_LEFT_MENU(self):
        # Get current left menu width
        width = self.frame_leftmenu.width()
        if width == 90:
            new_width = 186
        else:
            new_width = 90

        # Animate the transition
        self.animation = QPropertyAnimation(self.frame_leftmenu, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
        if new_width == 186 :
            self.label_HANWHA_SYTEMS.setStyleSheet("QLabel{border-image: url(:/ICON/resource/QuantumRED_MAIN/HANWHA_SYSTEMS.png);}")
        else :
            self.label_HANWHA_SYTEMS.setStyleSheet(
                "QLabel{border-image :url(:/ICON/resource/QuantumRED_MAIN/HANWHA_SYTEMS_MINI.png);}")

    # NUC 주기 타이머 func
    def Timer_start(self):
        self.SOC_CMD_SEND("1-REF_NUC")
        period = self.doubleSpinBox_NUC_P.value()
        self.timer = threading.Timer(period, self.Timer_start)
        self.timer.start()

    def NUC_AUTO_START(self):
        if self.NUC_AUTO :
            self.timer.cancel()
            self.NUC_AUTO = False
            self.PB_NUC_PERIOD.setStyleSheet(
                "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET.png);}"
                "QPushButton:hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_HOVER.png);}"
                "QPushButton:pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_PRESSED.png);}")
        else :
            self.Timer_start()
            self.NUC_AUTO = True
            self.PB_NUC_PERIOD.setStyleSheet(
                "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/NUC_PERIOD_STOP.png);}"
                "QPushButton:hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/NUC_PERIOD_STOP_HOVER.png);}"
                "QPushButton:pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/NUC_PERIOD_STOP_PRESSED.png);}")


    def REF_MOVE_SHOW(self):
        self.dlg = SOC_COMMAND_DIALOG()
        self.dlg.show()
        self.dlg.SOC_REF_MOVE_CMD.connect(self.SOC_SEND_REF_MOVE)

    @pyqtSlot(str)
    def SOC_SEND_REF_MOVE(self, str):
        self.SOC_CMD_SEND(str)
        if str == 'TRSM_REF_GUIDE_SAVE':
            self.textBrowser.append("GUIDE SAVE COMPLETE " + str)
        elif str == 'TRSM_REF_APPLY':
            self.textBrowser.append("APPLY COMPLETE " + str)
        else:
            self.textBrowser.append("MSG : REF MOVE "+str)

    def state_control(self, msg):
        self.textBrowser.append(msg)

    def SOC_BTN_INIT(self, state):
        if state == 'ON': set = True
        else : set = False
        self.Operating_pb.setEnabled(set)
        self.Processend_pb.setEnabled(set)
        self.Debugmode_pb.setEnabled(set)
        self.Viewermode_pb.setEnabled(set)
        self.Nuc1ref_pb.setEnabled(set)
        self.Tec_on_off_pb.setEnabled(set)
        self.Cem_on_off_pb.setEnabled(set)
        self.Nucview_pb.setEnabled(set)
        self.Rawview_pb.setEnabled(set)
        self.Partternview_pb.setEnabled(set)
    def LEFT_BTN_ACTIVE(self, type):

        self.PB_EZOOM_SET.setEnabled(False)
        self.PB_COLOR_SET.setEnabled(False)
        #TEMP 현재 CEM만 Enable! 21.04.21
        self.PB_CEM_SET.setEnabled(False)
        self.PB_NF_SET.setEnabled(False)
        if type == "EDGE":
            if self.EDGE_ACTIVE:
                self.PB_EDGE_SET.setEnabled(True)
                self.PB_EDGE.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/EDGE_OFF.png)}"
                    "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/EDGE_OFF_HOVER.png)}"
                    "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/EDGE_OFF_PRESSED.png)}")
                self.PB_EDGE_SET.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET.png)}"
                    "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_HOVER.png)}"
                    "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_PRESSED.png)}")
                self.EDGE_ACTIVE = False
            else :
                #self.SOC_CMD_SEND("EDGE_OFF")
                self.IMG_PROCESS.EDGE_ON = False
                self.PB_EDGE_SET.setEnabled(False)
                self.PB_EDGE.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/EDGE_ON.png)}"
                    "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/EDGE_ON_HOVER.png)}"
                    "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/EDGE_ON_PRESSED.png)}")
                self.PB_EDGE_SET.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_DISABLE.png)}")
                self.EDGE_ACTIVE = True

        elif type == "NF":
            if self.NF_ACTIVE:
                self.PB_NF_SET.setEnabled(True)
                self.PB_NF.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/NF_OFF.png)}"
                    "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/NF_OFF_HOVER.png)}"
                    "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/NF_OFF_PRESSED.png)}")
                self.PB_NF_SET.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET.png)}"
                    "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_HOVER.png)}"
                    "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_PRESSED.png)}")
                self.NF_ACTIVE = False
            else :
                #self.SOC_CMD_SEND("NF_OFF")
                self.IMG_PROCESS.NF_ON = False
                self.PB_NF_SET.setEnabled(False)
                self.PB_NF.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/NF_ON.png)}"
                    "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/NF_ON_HOVER.png)}"
                    "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/NF_ON_PRESSED.png)}")
                self.PB_NF_SET.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_DISABLE.png)}")
                self.NF_ACTIVE = True

        elif type == "EZOOM":
            if self.EZOOM_ACTIVE:
                self.PB_EZOOM_SET.setEnabled(True)
                self.PB_EZOOM.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/EZOOM_OFF.png)}"
                    "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/EZOOM_OFF_HOVER.png)}"
                    "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/EZOOM_OFF_PRESSED.png)}")
                self.PB_EZOOM_SET.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET.png)}"
                    "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_HOVER.png)}"
                    "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_PRESSED.png)}")
                self.EZOOM_ACTIVE = False
            else :
                #self.SOC_CMD_SEND("EZOOM_OFF")
                self.IMG_PROCESS.EZOOM_ON = False
                self.PB_EZOOM_SET.setEnabled(False)
                self.PB_EZOOM.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/EZOOM_ON.png)}"
                    "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/EZOOM_ON_HOVER.png)}"
                    "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/EZOOM_ON_PRESSED.png)}")
                self.PB_EZOOM_SET.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_DISABLE.png)}")
                self.EZOOM_ACTIVE = True

        elif type == "COLOR":
            if self.COLOR_ACTIVE:
                self.PB_COLOR_SET.setEnabled(True)
                self.PB_COLOR.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/COLOR_OFF.png)}"
                    "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/COLOR_OFF_HOVER.png)}"
                    "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/COLOR_OFF_PRESSED.png)}")
                self.PB_COLOR_SET.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET.png)}"
                    "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_HOVER.png)}"
                    "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_PRESSED.png)}")
                self.COLOR_ACTIVE = False
            else:
                self.SOC_CMD_SEND("COLOR_OFF")
                self.PB_COLOR_SET.setEnabled(False)
                self.PB_COLOR.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/COLOR_ON.png)}"
                    "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/COLOR_ON_HOVER.png)}"
                    "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/COLOR_ON_PRESSED.png)}")
                self.PB_COLOR_SET.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_DISABLE.png)}")
                self.COLOR_ACTIVE = True
        elif type == "CEM":
            if self.CEM_ACTIVE:
                self.PB_CEM_SET.setEnabled(True)
                self.PB_CEM.setStyleSheet(
                    "QPushButton{border-image: url(:/BTN/resource/BUTTON/CEM_OFF.png)}"
                    "QPushButton::hover{border-image :url(:/BTN/resource/BUTTON/CEM_OFF_HOVER.png}"
                    "QPushButton::pressed{border-image :url(:/BTN/resource/BUTTON/CEM_OFF_PRESSED.png)}")
                self.PB_CEM_SET.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET.png)}"
                    "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_HOVER.png)}"
                    "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_PRESSED.png)}")
                self.CEM_ACTIVE = False
            else:
                self.IMG_PROCESS.CEM_TYPE = '1' #Linear CEM
                self.PB_CEM_SET.setEnabled(False)
                self.PB_CEM.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/BUTTON/CEM_ON.png)}"
                    "QPushButton::hover{border-image :url(:/BTN/resource/BUTTON/CEM_ON_HOVER.png)}"
                    "QPushButton::pressed{border-image :url(:/BTN/resource/BUTTON/CEM_ON_PRESSED.png)}")
                self.PB_CEM_SET.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/SET_DISABLE.png)}")
                self.CEM_ACTIVE = True

    def CMD_CONTROL_BTN_ON_OFF(self, ON_OFF):

        self.PB_EDGE.setEnabled(ON_OFF)
        self.comboBox_EDGE.setEnabled(ON_OFF)
        self.PB_NF.setEnabled(ON_OFF)
        self.comboBox_NF.setEnabled(ON_OFF)
        self.PB_EZOOM.setEnabled(ON_OFF)
        self.comboBox_EZOOM.setEnabled(ON_OFF)

        if ON_OFF :
            self.PB_EDGE.setStyleSheet(
                "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/EDGE_ON.png)}"
                "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/EDGE_ON_HOVER.png)}"
                "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/EDGE_ON_PRESSED.png)}")
            self.PB_NF.setStyleSheet(
                "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/NF_ON.png)}"
                "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/NF_ON_HOVER.png)}"
                "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/NF_ON_PRESSED.png)}")
            self.PB_EZOOM.setStyleSheet(
                "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/EZOOM_ON.png)}"
                "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/EZOOM_ON_HOVER.png)}"
                "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/EZOOM_ON_PRESSED.png)}")
            '''
            self.PB_COLOR.setStyleSheet(
                "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/COLOR_ON.png)}"
                "QPushButton::hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/COLOR_ON_HOVER.png)}"
                "QPushButton::pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/COLOR_ON_PRESSED.png)}")
            '''

        else :

            self.PB_NF.setStyleSheet(
                "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/NF_ON_DISABLE.png)}")
            self.PB_EZOOM.setStyleSheet(
                "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/EZOOM_ON_DISABLE.png)}")
            self.PB_COLOR.setStyleSheet(
                "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/COLOR_ON_DISABLE.png)}")

    # ==================================================================================================================
    # USB DEVICE LIST GET
    # ==================================================================================================================
    @pyqtSlot(list)
    def GET_USB_DEVICE_LIST(self, device_list):
        self.device_list = device_list
        if self.prev_device_list == self.device_list:
            pass
        else:
            self.IMG_PROCESS.device_list = self.device_list
            self.cb_UVC_CH.clear()
            self.cb_UVC_CH.insertItems(0, self.device_list)
            for idx in range(len(self.device_list)):
                self.cb_UVC_CH.setItemIcon(idx, QIcon(":/ICON/resource/ICON/004-camera.png"))
        self.prev_device_list = self.device_list



    # ==================================================================================================================
    # TEMP Region OSD Draw
    # ==================================================================================================================
    def OSD_ON_OFF(self, OSD_TYPE):
        if OSD_TYPE == "TARGET":
            if self.TARGET_OSD_CHK.isChecked():
                self.TARGET_mouse_ing = True
                #QMessageBox.information(self, "MSG", "Set Target Region")
                self.IMG_PROCESS.OSD_TARGET = True

            else:
                self.IMG_PROCESS.OSD_TARGET = False
                self.IMG_PROCESS.OSD_TARGET_START = [0, 0]
                self.IMG_PROCESS.OSD_TARGET_END = [0, 0]
                self.TARGET_TEMP_DISPLAY_FLAG = False
                self.TARGET_OSD_TEMP.setText("")
        else:
            pass

    # ==================================================================================================================
    # Video REC / SNAPSHOT
    # ==================================================================================================================

    def SNAPSHOT(self):
        if self.IMG_PROCESS.Snap_save_file_folder == '':
            self.IMG_PROCESS.Snap_save_file_folder = QFileDialog.getExistingDirectory()

        if self.IMG_PROCESS.Snap_save_file_folder == '':
            pass
        else:
            snap_file_name = self.GET_SAVE_FILE_NAME("SNAP")
            self.IMG_PROCESS.Snap_save_file_path = self.IMG_PROCESS.Snap_save_file_folder + '/' + snap_file_name
            self.IMG_PROCESS.SNAP_Save_flag = True

    def GET_DIR_VIDEO_SNAP(self, type):
        if type == 'VIDEO':
            self.IMG_PROCESS.Video_save_file_folder = QFileDialog.getExistingDirectory()
            self.lineEdit_video.setText(self.IMG_PROCESS.Video_save_file_folder)
        else :
            self.IMG_PROCESS.Snap_save_file_folder = QFileDialog.getExistingDirectory()
            self.lineEdit_snap.setText(self.IMG_PROCESS.Snap_save_file_folder)
    def VIDEO_SAVE_STOP(self):
        if self.IMG_PROCESS.Video_Save_flag:
            self.IMG_PROCESS.Video_Save_flag = False
            self.IMG_PROCESS.Video_Stop_flag = True
            self.sb.showMessage('REC_STOP', 8000)
            self.Video_Save_BTN.setStyleSheet(
                "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/REC.png)}"
                "QPushButton:hover{border-image: url(:/BTN/resource/QuantumRED_MAIN/REC_HOVER.png)}"
                "QPushButton:pressed{border-image: url(:/BTN/resource/QuantumRED_MAIN/REC_PRESSED.png)}")
            self.textBrowser.append("Video_Save_Stop")
            QMessageBox.information(self, "MSG", "VIDEO REC STOP")
        else:
            if self.IMG_PROCESS.Video_save_file_folder == '':
                self.IMG_PROCESS.Video_save_file_folder = \
                    QFileDialog.getExistingDirectory()

            if self.IMG_PROCESS.Video_save_file_folder == '':
                pass
            else:
                video_file_name = self.GET_SAVE_FILE_NAME("VIDEO")
                self.IMG_PROCESS.Video_save_file_path = self.IMG_PROCESS.Video_save_file_folder + '/' + video_file_name
                self.IMG_PROCESS.VIDEO_SAVE_INIT()
                self.IMG_PROCESS.Video_Save_flag = True
                self.IMG_PROCESS.Video_Stop_flag = False
                self.Video_Save_BTN.setStyleSheet(
                    "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/REC_STOP.png)}"
                    "QPushButton:hover{border-image: url(:/BTN/resource/QuantumRED_MAIN/REC_STOP_HOVER.png)}"
                    "QPushButton:pressed{border-image: url(:/BTN/resource/QuantumRED_MAIN/REC_STOP_PRESSED.png)}")

            self.textBrowser.append("Video_Save_Start!")
            self.sb.showMessage('REC_ING', 8000)

    def GET_SAVE_FILE_NAME(self, file_name):
        index = 0
        if file_name == 'SNAP':
            file_list = os.listdir(self.IMG_PROCESS.Snap_save_file_folder)
            while True:
                name = file_name + str(index)
                if name + '.png' in file_list:
                    index += 1
                else:
                    break
            name = name + '.png'
        else :
            file_list = os.listdir(self.IMG_PROCESS.Video_save_file_folder)
            while True:
                name = file_name + str(index)
                if name + '.avi' in file_list:
                    index += 1
                else:
                    break
            name = name + '.avi'

        return name

    # ==================================================================================================================
    # Video Play/STOP
    # ==================================================================================================================
    def VIDEO_PLAY(self):
        self.IMG_PROCESS.Video_read_file_path = QFileDialog.getOpenFileName(self, "Open File","" ,"Video File(*.mp4 *.avi)")[0]
        self.IMG_PROCESS.simul_mode = True
        self.IMG_PROCESS.run = False
        self.CMD_CONTROL_BTN_ON_OFF(True)
        self.sb.showMessage('Video_Play', 8000)
        self.IMG_PROCESS.start()

    def VIDEO_STOP(self):
        self.IMG_PROCESS.simul_stop = True
        self.IMG_PROCESS.simul_mode = False
        self.CMD_CONTROL_BTN_ON_OFF(False)
        self.sb.showMessage('Video_Stop', 8000)



    # ==================================================================================================================
    # Qpiximg display video img
    # ==================================================================================================================

    @pyqtSlot(QPixmap)
    def FRAME_RAW_DISPLAY(self, img):
        self.image_label.setPixmap(img)
        self.IMG_PROCESS.img_label_width = self.image_label.width()
        self.IMG_PROCESS.img_label_height = self.image_label.height()
        self.cnt += 1
        if self.TARGET_TEMP_DISPLAY_FLAG:
            if self.cnt_target_avg == 5:
                self.TEMP_LIST.append(self.target_value_sum / (self.cnt_target_avg* 100))
                if len(self.TEMP_LIST) == 11:
                    self.TEMP_LIST.pop(0)
                    TEMP_AVG = self.TEMP_DIST_CAL(sum(self.TEMP_LIST) / len(self.TEMP_LIST), self.TEMP_DISTANCE_VAL)
                    self.TARGET_OSD_TEMP.setText(str(format(TEMP_AVG+ self.target_offset, '.2f')) + '℃')
                    self.target_value_sum = 0
                    self.cnt_target_avg = 0
            else :
                self.target_value_sum = self.target_value_sum + self.IMG_PROCESS.TARGET_ROI_MEAN
                self.cnt_target_avg += 1
        if self.TEC_TEMP_DISPLAY_FLAG:
            if self.cnt_tec_avg == 30:
                self.REF_OSD_TEMP.setText(str(format(self.tec_value_sum / (self.cnt_tec_avg * 100), '.2f'))+ '℃')
                self.tec_value_sum = 0
                self.cnt_tec_avg = 0
            else :
                self.tec_value_sum = self.tec_value_sum + self.IMG_PROCESS.TEC_ROI_MEAN
                self.cnt_tec_avg += 1
        if self.cnt == 30:
            if self.TEC_TEMP_DISPLAY_FLAG and self.TARGET_TEMP_DISPLAY_FLAG :
                self.lineEdit_diff.setText(str(format(self.IMG_PROCESS.TARGET_ROI_MEAN - self.IMG_PROCESS.TEC_ROI_MEAN, '.2f')))
            self.lineEdit_FPS.setText(str(format(self.IMG_PROCESS.FPS, '.2f')))
            self.lineEdit_WIDTH.setText(str(self.IMG_PROCESS.m_nXres))
            self.lineEdit_HEIGHT.setText(str(self.IMG_PROCESS.m_nYres))
            self.cnt = 0

    # TEMP DISTANCE CAL
    def TEMP_DIST_CAL(self, Temp, dist):
        TempResult = Temp * 1.049 + 0.1508 * dist - 1.679
        return TempResult

    def TEMP_DIST_VAL_SET(self):
        temp = self.comboBox_DISTANCE.currentText()
        self.TEMP_DISTANCE_VAL = int(temp.replace("m", ""))
    # ==================================================================================================================
    # USB Video connect/disconnect
    # ==================================================================================================================
    def START_STOP_FUNC(self):
        if self.run :  # start 수행 중일때
            self.CMD_CONTROL_BTN_ON_OFF(False)
            self.START_BTN.setStyleSheet(
                "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/CONNECT.png)}"
                "QPushButton:hover{border-image: url(:/BTN/resource/QuantumRED_MAIN/CONNECT_HOVER.png)}"
                "QPushButton:pressed{border-image: url(:/BTN/resource/QuantumRED_MAIN/CONNECT_PRESSED.png)}")
            self.IMG_PROCESS.run = False
            self.textBrowser.append("Get_Frame_STOP")
            self.run = False
            self.sb.showMessage('Frame Stop')

        else : # STOP 수행 중일때
            self.CMD_CONTROL_BTN_ON_OFF(True)
            self.START_BTN.setStyleSheet(
                "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/DISCONNECT.png)}"
                "QPushButton:hover{border-image: url(:/BTN/resource/QuantumRED_MAIN/DISCONNECT_HOVER.png)}"
                "QPushButton:pressed{border-image: url(:/BTN/resource/QuantumRED_MAIN/DISCONNECT_PRESSED.png)}")
            self.IMG_PROCESS.IF_mode = self.cb_mode_sel.currentText()
            time.sleep(0.1)
            self.textBrowser.append("Get_Frame_START")
            if self.IMG_PROCESS.IF_mode == "YUV422" or "Y-16":
                self.IMG_PROCESS.UVC_CH = self.device_list.index(self.cb_UVC_CH.currentText())
                self.textBrowser.append("Wait a Moment!....")
                self.sb.showMessage('Frame Running')
            self.textBrowser.append("Mode = " + self.IMG_PROCESS.IF_mode)
            self.run = True
            self.IMG_PROCESS.run = True
            self.IMG_PROCESS.start()

    #===================================================================================================================
    # TEMP CAL MOUSE EVENT
    #===================================================================================================================
    def GET_PIXEL_START(self, event):
        scale_x = self.image_label.width() / self.IMG_PROCESS.m_nXres
        scale_y = self.image_label.height() / self.IMG_PROCESS.m_nYres
        if self.TARGET_mouse_ing :
            self.IMG_PROCESS.OSD_TARGET_START = [int(event.pos().x()/scale_x), int(event.pos().y()/scale_y)]
            self.IMG_PROCESS.OSD_TARGET = False


    def GET_PIXEL_ING(self, event):
        scale_x = self.image_label.width() / self.IMG_PROCESS.m_nXres
        scale_y = self.image_label.height() / self.IMG_PROCESS.m_nYres
        if self.TARGET_mouse_ing:
           self.IMG_PROCESS.OSD_TARGET_END = [int(event.pos().x() / scale_x), int(event.pos().y() / scale_y)]
           self.IMG_PROCESS.OSD_TARGET = True

    def GET_PIXEL_END(self, event):
        scale_x = self.image_label.width() / self.IMG_PROCESS.m_nXres
        scale_y = self.image_label.height() / self.IMG_PROCESS.m_nYres
        if self.TARGET_mouse_ing:
           self.IMG_PROCESS.OSD_TARGET_END = [int(event.pos().x() / scale_x), int(event.pos().y() / scale_y)]
           self.IMG_PROCESS.OSD_TARGET = True
           self.TARGET_TEMP_DISPLAY_FLAG = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QuantumRED_MAIN_TEMP()
    MainWindow.show()
    sys.exit(app.exec_())



