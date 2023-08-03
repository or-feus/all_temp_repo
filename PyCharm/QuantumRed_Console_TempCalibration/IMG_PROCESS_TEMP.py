
import time

import cv2
import numpy as np
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from PyQt5.QtGui import QImage, QPixmap



class IMAGE_PROCESS_TEMP(QThread, QObject):
    frame_signal1 = pyqtSignal(QPixmap)
    frame_signal2 = pyqtSignal(QPixmap)
    serial_state = pyqtSignal(bool)
    state_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.working = True
        self.auto_check = True
        self.simul_mode = False
        self.Thermal_mode = False
        self.m_nXres = 320
        self.m_nYres = 240
        self.data_mode = 8
        self.run = False
        self.IF_mode = "YUV422"
        self.UVC_CH = 0
        self.Mat_list = dict()
        self.Video_Save_flag = False
        self.Video_Stop_flag = False
        self.SNAP_Save_flag = False
        self.Video_read_file_path = ''
        self.Video_save_file_path = ''
        self.Snap_save_file_path = ''
        self.Video_save_file_folder = ''
        self.Snap_save_file_folder = ''
        self.video_file_name = ''
        self.snap_file_name = ''
        self.FPS = 0
        self.simul_stop = False
        self.OSD_TARGET = False
        self.OSD_TARGET_START = [0, 0]
        self.OSD_TARGET_END = [0, 0]
        #self.device_list = []
        self.TARGET_ROI_MEAN = 0
        self.TEC_ROI_MEAN = 0
        # img_label_size
        self.img_label_width = 640
        self.img_label_height = 480
        # TEMP_VALUE BUFFER
        self.TEMP_LIST = []
        self.CEM_TYPE = '1'
        self.GET_TYPE = 'AVG'
        #sharpning Filter
        self.sharpening_mask1 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        self.sharpening_mask2 = np.array([[1, 1, 1], [1, -7, 1], [1, 1, 1]])
        self.sharpening_mask3 = np.array([[-1, -1, -1,-1, -1], [-1, 2, 2, 2, -1], [-1, 2, 8, 2, -1], [-1, 2, 2, 2, -1], [-1, -1, -1, -1, -1]])/8.0
        # Average Filter
        self.AVG_mask = np.array([[0.04, 0.04, 0.04, 0.04, 0.04], [0.04, 0.04, 0.04, 0.04, 0.04], [0.04, 0.04, 0.04, 0.04, 0.04], [0.04, 0.04, 0.04, 0.04, 0.04], [0.04, 0.04, 0.04, 0.04, 0.04]])

        # IMG_PROC_VIEWER
        self.EDGE_ON = False
        self.EDGE_Type = "EDGE_MID"
        self.NF_ON = False
        self.NF_Type = "NF_MID"
        self.EZOOM_ON = False
        self.EZOOM_Type = "EZOOM_2X"
        self.COLOR_ON = False
        self.COLOR_Type = "COLOR1"

    def run(self):
        while self.working:
            if self.simul_mode:
                self.uvc_cap = cv2.VideoCapture(self.Video_read_file_path)
                self.FPS = int(self.uvc_cap.get(5))
                prev_time = 0
                while (self.uvc_cap.isOpened()):
                    if self.simul_stop:
                        break
                    ret, frame = self.uvc_cap.read()
                    if ret:
                        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        image = self.CEM_PROC(image)
                        image = self.IMG_PROC_ETC(image)
                        if self.NF_ON:
                            if self.NF_Type == "NF_1":
                                image = cv2.fastNlMeansDenoising(image, None, 3, 7, 21)
                        qt_img1 = self.convert_cv_qt(image)
                        self.frame_signal1.emit(qt_img1)
                        if self.SNAP_Save_flag:
                            cv2.imwrite(self.Snap_save_file_path, image)
                            self.state_signal.emit("Snap_IMG Save Complete!")
                            self.SNAP_Save_flag = False
                        if cv2.waitKey(10) == ord('q'):
                            break
                    else:
                        self.uvc_cap.release()
                        self.simul_mode = False
                        break
                self.uvc_cap.release()
                cv2.destroyAllWindows()

            elif self.IF_mode == "Y-16":
                # cv2.CAP_DSHOW 카메라 사용 시 사용할 백엔드 지정 없으면 워닝 메시지 우루루루루....
                self.uvc_cap = cv2.VideoCapture(int(self.UVC_CH), cv2.CAP_DSHOW)

                self.uvc_cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('Y', '1', '6', ' '))
                rtn = self.uvc_cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)
                if rtn: self.state_signal.emit("Y-16_CONNECT!")
                else : self.state_signal.emit("Y-16_FAIL!")
                time.sleep(1)
                prev_time = 0
                while (self.uvc_cap.isOpened()):
                    ret, frame = self.uvc_cap.read()
                    #print(frame.max(), frame.min())
                    if self.run:
                        if ret:
                            current_time = time.time()
                            self.FPS = 1. / (current_time - prev_time)
                            self.m_nYres, self.m_nXres = frame.shape[0], frame.shape[1]
                            image = np.zeros((self.m_nYres, self.m_nXres))
                            frame_test = frame.copy()
                            frame_test = np.clip(frame_test, 0, 4095)
                            frame_test = self.CEM_PROC(frame_test)
                            frame_test = self.IMG_PROC_ETC(frame_test)
                            image = cv2.normalize(frame_test, image, 0, 255, cv2.NORM_MINMAX)
                            image = image.astype("uint8")
                            if self.NF_ON:
                                if self.NF_Type == "NF_2":
                                    image = cv2.fastNlMeansDenoising(image, None, 3, 7, 21)

                            if self.OSD_TARGET:
                                image = self.OSD_DRAW(image)
                                try:
                                    if self.GET_TYPE == 'AVG':
                                        self.TARGET_ROI_MEAN = frame[self.OSD_TARGET_START[1]:self.OSD_TARGET_END[1],
                                                               self.OSD_TARGET_START[0]:self.OSD_TARGET_END[0]].mean()
                                    if self.GET_TYPE == 'MAX':
                                        self.TARGET_ROI_MEAN = np.max(frame[self.OSD_TARGET_START[1]:self.OSD_TARGET_END[1],
                                                               self.OSD_TARGET_START[0]:self.OSD_TARGET_END[0]])
                                    if self.GET_TYPE == 'MIN':
                                        self.TARGET_ROI_MEAN = np.min(frame[self.OSD_TARGET_START[1]:self.OSD_TARGET_END[1],
                                                               self.OSD_TARGET_START[0]:self.OSD_TARGET_END[0]])
                                except:
                                    self.TARGET_ROI_MEAN = 0
                                    self.TEC_ROI_MEAN = 0
                                    print("ERROR")

                            qt_img1 = self.convert_cv_qt(image)
                            self.frame_signal1.emit(qt_img1)

                            if self.Video_Save_flag:
                                self.Video_out.write(image)

                            if self.Video_Stop_flag:
                                self.Video_out.release()
                                self.state_signal.emit("Video Save Complete!")
                                self.Video_Stop_flag = False
                            if self.SNAP_Save_flag:
                                try:
                                    cv2.imwrite(self.Snap_save_file_path, image)
                                    self.state_signal.emit("Snap_IMG Save Complete!")
                                    self.SNAP_Save_flag = False
                                except:
                                    pass
                            prev_time = current_time
                            time.sleep(0.01)
                        else:
                            pass
                    else:
                        self.uvc_cap.release()
                        self.IF_mode = ''
                        break
                self.uvc_cap.release()
                self.IF_mode = ''

            elif self.IF_mode == "YUV422":
                self.uvc_cap = cv2.VideoCapture(int(self.UVC_CH), cv2.CAP_DSHOW)

                self.state_signal.emit("YUV422_CONNECT")
                prev_time = 0
                while (self.uvc_cap.isOpened()):
                    ret, frame = self.uvc_cap.read()
                    if self.run:
                        if ret:
                            current_time = time.time()
                            self.FPS = int(1 / (current_time - prev_time))
                            self.m_nXres, self.m_nYres = frame.shape[1], frame.shape[0]
                            image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                            if self.OSD_TARGET:
                                image = self.OSD_DRAW(image)
                            qt_img1 = self.convert_cv_qt(image)
                            self.frame_signal1.emit(qt_img1)

                            if self.Video_Save_flag:
                                self.Video_out.write(image)
                            if self.Video_Stop_flag:
                                self.Video_out.release()
                                self.state_signal.emit("Video Save Complete!")
                                self.Video_Stop_flag = False
                            if self.SNAP_Save_flag:
                                cv2.imwrite(self.Snap_save_file_path, image)
                                self.state_signal.emit("Snap_IMG Save Complete!")
                                self.SNAP_Save_flag = False
                            prev_time = current_time
                            time.sleep(0.01)
                        else:
                            pass
                    else:
                        self.uvc_cap.release()
                        self.IF_mode = ''
                        break
                self.uvc_cap.release()
                self.IF_mode = ''

    def stop(self):
        self.working = False
        self.wait()
        print("IMG_PROC_END!")
        self.wait(2000)

    def EZOOM(self, img, zoom_size):
        img = cv2.resize(img, dsize=(img.shape[0]*zoom_size, img.shape[1]*zoom_size), interpolation=cv2.INTER_CUBIC)
        center = (int(img.shape[0]/2), int(img.shape[1]/2))
        crop_scale = (int(center[0]/zoom_size), int(center[1]/zoom_size))
        img = img[crop_scale[0]: (center[0] + crop_scale[0]), crop_scale[1]:(center[1] + crop_scale[1])]
        return img

    def IMG_PROC_ETC(self, img):
        # Noise Filter
        if self.EDGE_ON:
            if self.EDGE_Type == "EDGE_1":
                img = cv2.filter2D(img, -1, self.sharpening_mask1)
            if self.EDGE_Type == "EDGE_2":
                img = cv2.filter2D(img, -1, self.sharpening_mask2)
            if self.EDGE_Type == "EDGE_3":
                img = cv2.filter2D(img, -1, self.sharpening_mask3)
        # EZOOM
        if self.EZOOM_ON:
            if self.EZOOM_Type == "EZOOM_2X":
                img = self.EZOOM(img, 2)
            if self.EZOOM_Type == "EZOOM_4X":
                img = self.EZOOM(img, 4)

        return img

    def OSD_DRAW(self, img):
        try:
            img_RGB = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            if self.OSD_TARGET:
                cv2.rectangle(img_RGB, tuple(self.OSD_TARGET_START), tuple(self.OSD_TARGET_END), (0, 0, 255), 1)
        except:
            img_RGB = img
            if self.OSD_TARGET:
                cv2.rectangle(img_RGB, tuple(self.OSD_TARGET_START), tuple(self.OSD_TARGET_END), (0, 0, 255), 1)
        return img_RGB

    def CEM_PROC(self, img):
        if self.CEM_TYPE == '1':
            #Linear
            img_cem = img
        elif self.CEM_TYPE == '2':
            # CLAHE
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(5, 5))
            img_cem = clahe.apply(img)
        else:
            pass
        return img_cem

    def VIDEO_SAVE_INIT(self):
        w = round(self.m_nXres)
        h = round(self.m_nYres)
        fps = int(self.FPS)
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        delay = round(1000 / fps)
        self.Video_out = cv2.VideoWriter(self.Video_save_file_path, fourcc, fps, (w, h), isColor=False)


    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        # 컬러 이미지일 경우
        if cv_img.shape[-1] == 3:
            image = cv_img.copy()
            h, w, ch = image.shape
            bytes_per_line = w * ch
            convert_to_Qt_format = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)


        # GRAYSCALE 경우
        else:
            image = cv_img.copy()
            h, w = image.shape
            bytes_per_line = w
            convert_to_Qt_format = QImage(image.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
        return QPixmap.fromImage(convert_to_Qt_format)