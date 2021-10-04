# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
import cv2
import numpy as np
import copy

from fid.detect_package import PackageDetector


class ROI:
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    save = False

    def __str__(self):
        return f'{(self.x0, self.y0)}, {(self.x1, self.y1)}'


class Label(QLabel):
    roi = ROI()
    roi2 = ROI()
    id_roi = 0
    flag = False

    # Mouse click event
    def mousePressEvent(self, event):
        self.flag = True
        if self.id_roi == 0:
            self.roi.x0 = event.x()
            self.roi.y0 = event.y()
        elif self.id_roi == 1:
            self.roi2.x0 = event.x()
            self.roi2.y0 = event.y()

    # Mouse release event
    def mouseReleaseEvent(self, event):
        self.flag = False

    # Mouse movement events
    def mouseMoveEvent(self, event):
        if self.flag:
            if self.id_roi == 0:
                self.roi.x1 = event.x()
                self.roi.y1 = event.y()
                self.roi.save = True
            elif self.id_roi == 1:
                self.roi2.x1 = event.x()
                self.roi2.y1 = event.y()
                self.roi2.save = True
            self.update()

    # Draw events
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        if self.id_roi == 0 or self.roi.save:
            rect = QRect(self.roi.x0, self.roi.y0, abs(self.roi.x1 - self.roi.x0), abs(self.roi.y1 - self.roi.y0))
            pen = Qt.red
            painter.setPen(QPen(pen, 2, Qt.SolidLine))
            painter.drawRect(rect)
        if self.id_roi == 1 or self.roi2.save:
            rect = QRect(self.roi2.x0, self.roi2.y0, abs(self.roi2.x1 - self.roi2.x0), abs(self.roi2.y1 - self.roi2.y0))
            pen = Qt.green
            painter.setPen(QPen(pen, 2, Qt.SolidLine))
            painter.drawRect(rect)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(761, 436)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = Label(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 20, 600, 400))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(30, 40, 95, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton.setFont(font)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(30, 70, 95, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 100, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 130, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 160, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(30, 190, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        MainWindow.setCentralWidget(self.centralwidget)
        img = cv2.imread('2.jpg')
        height, width, bytesPerComponent = img.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        QImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        self.label.setPixmap(pixmap)
        self.label.setCursor(Qt.CrossCursor)

        self.detector = PackageDetector()
        self.roi = ROI()
        self.roi2 = ROI()

        self.radioButton.clicked.connect(self.clicked_radio)
        self.radioButton_2.clicked.connect(self.clicked_radio)

        self.pushButton.clicked.connect(self.btn1_clicked)
        self.pushButton_2.clicked.connect(self.btn2_clicked)
        self.pushButton_3.clicked.connect(self.btn3_clicked)
        self.pushButton_4.clicked.connect(self.btn4_clicked)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def clicked_radio(self):
        if self.radioButton.isChecked():
            self.label.id_roi = 0
        elif self.radioButton_2.isChecked():
            self.label.id_roi = 1

    def btn1_clicked(self):
        self.detector.system.connect_camera(0)
        self.detector.system.set_modbus_client(host='192.168.48.32', port=502)
        self.label.roi2.x0 = 0
        self.label.roi2.y0 = 0
        self.label.roi2.x1 = 0
        self.label.roi2.y1 = 0
        self.image = cv2.resize(self.detector.system.get_image(), (600, 400))
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        height, width, bytesPerComponent = self.image.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB, self.image)
        QImg = QImage(self.image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        self.label.resize(pixmap.size())
        self.label.setPixmap(pixmap)

    def btn2_clicked(self):
        self.roi = copy.copy(self.label.roi)
        print(self.roi)
        self.label.roi.x0 = 0
        self.label.roi.y0 = 0
        self.label.roi.x1 = 0
        self.label.roi.y1 = 0
        print(self.roi)
        image = copy.copy(self.image[self.roi.y0:self.roi.y1, self.roi.x0:self.roi.x1])
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img = self.detector.detect(img)
        height, width, bytesPerComponent = img.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        QImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        self.label.resize(pixmap.size())
        self.label.setPixmap(pixmap)

    def btn3_clicked(self):
        self.roi2 = copy.copy(self.label.roi2)
        print(self.roi, self.roi2)

    def btn4_clicked(self):
        self.detector.system.connect_camera(0)
        self.detector.system.set_modbus_client(host='192.168.48.32', port=502)
        while True:
            image = cv2.resize(self.detector.system.get_image(), (600, 400))
            image = image[self.roi.y0:self.roi.y1, self.roi.x0:self.roi.x1]
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = self.detector.detect(image, self.roi2)
            cv2.imshow('Result', image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                cv2.destroyAllWindows()
                break
            elif key == ord('p'):
                break

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.radioButton.setText(_translate("MainWindow", "ROI"))
        self.radioButton_2.setText(_translate("MainWindow", "Feature"))
        self.pushButton.setText(_translate("MainWindow", "Get Image"))
        self.pushButton_2.setText(_translate("MainWindow", "Get Feature"))
        self.pushButton_3.setText(_translate("MainWindow", "Save"))
        self.pushButton_4.setText(_translate("MainWindow", "Start"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())