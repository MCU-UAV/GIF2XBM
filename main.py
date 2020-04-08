import sys
from MainWindows import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
from ConvertXBM import *
from PIL import Image
# from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
import cv2
from PyQt5 import QtWidgets
import os.path

#
# def btnDealOpenFile(self):
#     openfile_name = QFileDialog.getOpenFileName(self,)
#     print("hello")
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainWindow = QMainWindow()
#     ui = MainWindows.Ui_MainWindow()
#     ui.setupUi(mainWindow)
#     mainWindow.show()
#     ui.pushButton_openFile.clicked.connect(btnDealOpenFile)
#     sys.exit(app.exec_())



class MainForm(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.read_flag = False
        self.img_scale = 0
        self.new_width = 0
        self.new_height = 0
        self.pushButton_openFile.clicked.connect(self.btnDealOpenFile)
        self.pushButton_generate.clicked.connect(self.btnDealGenerate)
        self.lineEdit_sizeX.editingFinished.connect(lambda: self.lineEditDealSize(self.lineEdit_sizeX.objectName()))
        self.lineEdit_sizeY.editingFinished.connect(lambda: self.lineEditDealSize(self.lineEdit_sizeY.objectName()))
        self.horizontalSlider.valueChanged.connect(self.sliderDealFrame)
        self.horizontalSlider.setDisabled(True)
    def btnDealOpenFile(self):
        img_path ,img_type= QFileDialog.getOpenFileName(self,'选择文件','','GIF Files(*.gif);;IMG Files(*.jpg;*.png;'
                                                                    '*.bmp;*.ico)')
        if img_path == b'':
            return
        self.img = Image.open(img_path)
        self.read_flag = True
        self.animation_name = os.path.basename(self.img.filename).split('.')[0]
        print(self.img.size[0], self.img.format)
        self.new_width = self.img.size[0]
        self.new_height = self.img.size[1]
        self.img_scale = self.img.size[0] / self.img.size[1]
        self.lineEdit_dirPath.setText(self.img.filename)
        self.lineEdit_sizeX.setText(str(self.img.size[0]))
        self.lineEdit_sizeY.setText(str(self.img.size[1]))
        self.lineEdit_minFrame.setText("1")

        self.horizontalSlider.setMinimum(1)

        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setValue(1)
        self.horizontalSlider.setTickPosition(QSlider.TicksBelow)
        self.horizontalSlider.setTickInterval(1)

        self.label_originalSize.setText(str(self.img.size))

        if(self.img.format == 'GIF'):
            self.lineEdit_maxFrame.setText(str(self.img.n_frames))
            self.horizontalSlider.setMaximum(self.img.n_frames)
            self.label_currendFrame.setText("1/" + str(self.img.n_frames))
            self.label_frameNum.setText(str(self.img.n_frames))
            self.movie = QMovie(img_path)
            #self.label_origialGif.setScaledContents(False)
            self.label_originalGif.setMovie(self.movie)

            self.movie.start()
        else:
            self.horizontalSlider.setDisabled(True)
            self.img.seek(0)
            self.lineEdit_maxFrame.setText("1")
            new = Image.new("RGBA", self.img.size)
            new.paste(self.img)
            rawdata = new.tobytes('raw', 'RGBA')
            image = QImage(rawdata, new.size[0], new.size[1], QImage.Format_RGBX8888)
            pix = QPixmap.fromImage(image).scaled(QSize(self.new_width, self.new_height))
            # pix = QPixmap.fromImage(self.img).scaled(QSize(self.new_width,self.new_height))
            # self.label_originalGif.setScaledContents(True)
            self.label_originalGif.setPixmap(pix)
        # temp = QtGui.QImage('C:/Users/imgDir/test.jpg')
        # print(temp.isNull())
        # jpg = QtGui.QPixmap("D:/test.jpg").scaled(self.label_origialGif.width(), self.label_origialGif.height())
        # self.label_origialGif.setScaledContents(True)
        # self.label_origialGif.setPixmap(jpg)
       #print(img_path)
    def lineEditDealSize(self,linetextname):
        if self.read_flag:
            if self.radioButton_keepScale.isChecked():
                if linetextname == 'lineEdit_sizeX':
                    self.new_width = int(self.lineEdit_sizeX.text())
                    self.new_height = int(self.new_width / self.img_scale)
                    self.lineEdit_sizeY.setText(str(self.new_height))

                else:
                    self.new_height = int(self.lineEdit_sizeY.text())
                    self.new_width = int(self.new_height * self.img_scale)
                    self.lineEdit_sizeX.setText(str(self.new_width))
            else:
                self.new_width = int(self.lineEdit_sizeX.text())
                self.new_height = int(self.lineEdit_sizeY.text())
                self.lineEdit_sizeX.setText(str(self.new_width))
                self.lineEdit_sizeY.setText(str(self.new_height))
            if (self.img.format == 'GIF'):
                self.label_originalGif.clear()
                # self.movie.stop()
                self.movie.setScaledSize(QSize(self.new_width,self.new_height))
                self.label_originalGif.setMovie(self.movie)
                self.movie.start()
            else:
                self.label_originalGif.clear()
                self.img.seek(0)
                new = Image.new("RGBA", self.img.size)
                new.paste(self.img)
                rawdata = new.tobytes('raw', 'RGBA')
                image = QImage(rawdata, new.size[0], new.size[1], QImage.Format_RGBX8888)
                pix = QPixmap.fromImage(image).scaled(QSize(self.new_width,self.new_height))
                #pix = QPixmap.fromImage(self.img).scaled(QSize(self.new_width,self.new_height))
                #self.label_originalGif.setScaledContents(True)
                self.label_originalGif.setPixmap(pix)

    def sliderDealFrame(self):
        if self.read_flag:
            #self.label_currentFrame_Win.clearMask()
            self.horizontalSlider.setDisabled(False)
            current_img = self.horizontalSlider.value()
            self.img.seek(current_img-1)
            new = Image.new("RGBA", self.img.size)
            new.paste(self.img)
            rawdata = new.tobytes('raw','RGBA')
            image = QImage(rawdata, new.size[0], new.size[1], QImage.Format_RGBX8888)
            pix = QPixmap.fromImage(image).scaled(self.label_currentFrame_Win.width(), self.label_currentFrame_Win.height())
            # qimg = QImage(new.tostring('raw', 'RGBA'))
            # pix = QPixmap.fromImage(new).scaled(self.new_width, self.new_height)
            self.label_currentFrame_Win.setScaledContents(True)
            self.label_currentFrame_Win.setPixmap(pix)
            if (self.img.format == 'GIF'):
                self.label_currendFrame.setText(str(current_img)+"/" + str(self.img.n_frames))
            else:
                self.label_currendFrame.setText("1/1")

    def btnDealGenerate(self):
        if self.read_flag:
            self.textBrowser.clear()
            if self.radioButton_invBits.isChecked():
                inv = 1
            else:
                inv = 0
            ccode = ConvertXBM(self.img,self.new_width,self.new_height)
            frame_start = int(self.lineEdit_minFrame.text())
            frame_end = int(self.lineEdit_maxFrame.text())
            if (self.img.format == 'GIF'):
                framesum,bufsize,rescode = ccode.gif2XBM(frame_start,frame_end,inv=inv)
            else:
                bufsize, rescode = ccode.img2XBM(self.img,self.new_width,self.new_height,inv=inv)
                rescode = '{'+rescode+'}'
                framesum = 1

            codepre = '#define u8g2_{}_width {}\n#define u8g2_{}_height {}\n#define u8g2_{}_frames {}\n' \
                      'static const unsigned char u8g2_{}_bmp [{}][{}] U8X8_PROGMEM\n'.format(self.animation_name,
                                                                                              self.new_width,
                                                                                              self.animation_name,
                                                                                              self.new_height,
                                                                                              self.animation_name,
                                                                                              framesum,
                                                                                              self.animation_name,
                                                                                              framesum,bufsize)

            self.textBrowser.setText(codepre + rescode+';')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainForm()
    win.show()
    sys.exit(app.exec_())
