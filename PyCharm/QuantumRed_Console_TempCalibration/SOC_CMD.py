import time

from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QDialog
import os

os.system('Pyrcc5 SOC_Dialog.qrc -o SOC_Dialog_rc.py')
dialog_class = uic.loadUiType("SOC_COMMAND.ui")[0]
class SOC_COMMAND_DIALOG(QDialog, dialog_class, QObject):
    SOC_REF_MOVE_CMD = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_widget()
        self.Guide_ON = False

    def closeEvent(self, event):
        self.close()

    def init_widget(self):
        # SOC REF MOVE CMD
        self.PB_REF_UP_2.setAutoRepeat(True)
        self.PB_REF_UP_2.setAutoRepeatDelay(100)
        self.PB_REF_UP_2.setAutoRepeatInterval(100)
        self.PB_REF_RIGHT_2.setAutoRepeat(True)
        self.PB_REF_RIGHT_2.setAutoRepeatDelay(100)
        self.PB_REF_RIGHT_2.setAutoRepeatInterval(100)
        self.PB_REF_LEFT_2.setAutoRepeat(True)
        self.PB_REF_LEFT_2.setAutoRepeatDelay(100)
        self.PB_REF_LEFT_2.setAutoRepeatInterval(100)
        self.PB_REF_DOWN.setAutoRepeat(True)
        self.PB_REF_DOWN.setAutoRepeatDelay(100)
        self.PB_REF_DOWN.setAutoRepeatInterval(100)
        self.PB_REF_UP_2.clicked.connect(lambda : self.SOC_REF_MOVE_SEND("TRSM_REF_GUIDE_UP"))
        self.PB_REF_RIGHT_2.clicked.connect(lambda: self.SOC_REF_MOVE_SEND("TRSM_REF_GUIDE_RIGHT"))
        self.PB_REF_LEFT_2.clicked.connect(lambda: self.SOC_REF_MOVE_SEND("TRSM_REF_GUIDE_LEFT"))
        self.PB_REF_DOWN.clicked.connect(lambda: self.SOC_REF_MOVE_SEND("TRSM_REF_GUIDE_DOWN"))
        self.PB_GUIDE.clicked.connect(self.REF_GUIDE_ON_OFF)
        self.PB_GUIDE_SAVE.clicked.connect(lambda: self.SOC_REF_MOVE_SEND("TRSM_REF_GUIDE_SAVE"))
        #self.PB_APPLY.clicked.connect(lambda: self.SOC_REF_MOVE_SEND("TRSM_REF_APPLY"))
    '''
    def SOC_REF_MOVE_SEND(self, CMD, Auto_repeat):
        while True
            if self.Auto_repeat:
                self.SOC_REF_MOVE_CMD.emit(CMD)
            else :
                break
            time.sleep(0.3)
    '''

    def SOC_REF_MOVE_SEND(self, CMD):
        self.SOC_REF_MOVE_CMD.emit(CMD)


    def REF_GUIDE_ON_OFF(self):
        if self.Guide_ON :
            self.SOC_REF_MOVE_SEND("TRSM_REF_GUIDE_OFF")
            self.Guide_ON = False
            self.PB_GUIDE.setStyleSheet(
                "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/GUIDE_ON.png);}"
                "QPushButton:hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/GUIDE_ON_HOVER.png);}"
                "QPushButton:pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/GUIDE_ON_PRESSED.png);}")
        else:
            self.SOC_REF_MOVE_SEND("TRSM_REF_GUIDE_ON")
            self.Guide_ON = True
            self.PB_GUIDE.setStyleSheet(
                "QPushButton{border-image :url(:/BTN/resource/QuantumRED_MAIN/GUIDE_OFF.png);}"
                "QPushButton:hover{border-image :url(:/BTN/resource/QuantumRED_MAIN/GUIDE_OFF_HOVER.png);}"
                "QPushButton:pressed{border-image :url(:/BTN/resource/QuantumRED_MAIN/GUIDE_OFF_PRESSED.png);}")