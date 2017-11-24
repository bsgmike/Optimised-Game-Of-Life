#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
ver = sys.version
print("We're running version ", ver)

# if ver > 3:
import sip
# switch on QString in Python3
sip.setapi('QString', 1)

try:
    from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QT_VERSION_STR, QPoint, QDir, QEvent

    from PyQt5.QtGui import QImage, QPixmap, QPainterPath, QPainter, QFont, QIcon, QPalette, QColor, QLinearGradient

    from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
        QLabel, QFrame, QTextEdit,QHBoxLayout, QVBoxLayout, QMainWindow, QAction, QTableView, QTabWidget, QMessageBox, \
        QComboBox, QStyleFactory, QCheckBox, QFileDialog
except ImportError:
    try:
        from PyQt4.QtCore import Qt, QRectF, pyqtSignal, QT_VERSION_STR
        from PyQt4.QtGui import *
    except ImportError:
        raise ImportError("ImageViewerQt: Requires PyQt5 or PyQt4.")

from PIL import Image
from PIL.ImageQt import ImageQt




class InformationLabel(QWidget):
    def __init__(self, legend):
        super(InformationLabel, self).__init__()
        self.myLayout = QHBoxLayout()
        self.myLayout.setAlignment(Qt.AlignLeft)
        self.myLegend = QLabel()
        self.myLegend.setFixedWidth(70)
        self.myText = QLineEdit()
        self.myText.setFixedWidth(200)
        self.myLegend.setText(legend)
        self.myText.setText(legend)
        self.myLayout.addWidget(self.myLegend)
        self.myLayout.addWidget(self.myText)
        self.setLayout(self.myLayout)

    def updateText(self, newText):
        self.myText.setText(newText)

class LabelledButton(QWidget):
    def __init__(self, legend):
        super(LabelledButton, self).__init__()

        self.setFixedHeight(45)
        self.setFixedWidth(400)
        pal = self.palette()
        pal.setColor(self.backgroundRole(), QColor('#ffffff'))
        pal.setColor(self.foregroundRole(), QColor('#e65555'))#6600cc
        self.setPalette(pal)
        self.setAutoFillBackground(True)
        self.myLayout = QHBoxLayout(self)
        self.show()

        self.myButton = QPushButton()
        self.myButton.setFixedWidth(50)

        self.myLegend = QLabel()
        font = QFont()
        font.setFamily('SansSerif')
        font.setBold(True)
        # newfont = QFont("SansSerif", 12, QFont.Bold)
        newfont = QFont("MS Shell Dlg 2", 10)
        self.myLegend.setFont(newfont)
        labelpal = self.myLegend.palette()
        labelpal.setColor(self.foregroundRole(), QColor('#ff0000'))  # 6600cc
        self.myLegend.setPalette(labelpal)

        self.myLegend.setFixedWidth(200)
        self.myLegend.setText(legend)

        self.myLayout.addWidget(self.myLegend)
        self.myLayout.addWidget(self.myButton)
        self.setLayout(self.myLayout)

    def updateText(self, newText):
        self.myText.setText(newText)

    def paintEvent(self, ev):
        margin = 4
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing);
        gradient = QLinearGradient(QRectF(self.rect()).topLeft(),
                                         QRectF(self.rect()).bottomLeft())

        gradient.setColorAt(0.0, QColor("#3399ff"))
        gradient.setColorAt(0.4, QColor("#b3d9ff"))
        gradient.setColorAt(0.7, QColor("#3399ff"))
        # painter.setBrush(QColor("#b3ffff"))
        # painter.setBrush(gradient)
        painter.setBrush(QColor("#e6ffff"))
        painter.drawRoundedRect(margin, margin, self.width()-(2*margin), self.height()-(2*margin), 8.0, 8.0)

class LabelledButton2(QWidget):
    def __init__(self, legend):
        super(LabelledButton2, self).__init__()

        self.setFixedHeight(45)
        self.setFixedWidth(400)
        pal = self.palette()
        pal.setColor(self.backgroundRole(), QColor('#ffffff'))
        pal.setColor(self.foregroundRole(), QColor('#000000'))#6600cc
        self.setPalette(pal)
        self.setAutoFillBackground(True)
        self.myLayout = QHBoxLayout(self)
        self.myLayout.setAlignment(Qt.AlignLeft)
        self.show()

        self.myButton = QPushButton()
        self.myButton.setFixedWidth(80)

        self.myLegend = QLabel()
        self.myLegend.setFrameStyle(QFrame.Box)
        font = QFont()
        font.setFamily('SansSerif')
        font.setBold(True)

        newfont = QFont("MS Shell Dlg 2", 10)
        self.myLegend.setFont(newfont)
        labelpal = self.myLegend.palette()
        labelpal.setColor(self.foregroundRole(), QColor('#000000'))
        self.myLegend.setPalette(labelpal)

        self.myLegend.setFixedWidth(250)

        self.myButton.setText(legend)

        self.myLayout.addWidget(self.myLegend)
        self.myLayout.addWidget(self.myButton)
        self.setLayout(self.myLayout)

    def updateText(self, newText):
        self.myLegend.setText(newText)

    def paintEvent(self, ev):
        margin = 4
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing);

        painter.setBrush(QColor("#ffffff"))
        painter.drawRect(0, 0, self.width(), self.height())

class ImageLabel(QLabel):
    def __init__(self, img):
        super(ImageLabel, self).__init__()
        self.setFrameStyle(QFrame.StyledPanel)
        self.setMaximumHeight(240)
        self.setMaximumWidth(320)
        self.setMinimumHeight(240)
        self.size = 320, 240
        self.im = Image.open(img)
        self.im.thumbnail(self.size)

    def paintEvent(self, event):
        # size = self.size()
        painter = QPainter(self)
        point = QPoint(0,0)
        myQtImage = ImageQt(self.im)
        pixmap = QPixmap.fromImage(myQtImage)
        label = QLabel('', self)
        label.setPixmap(pixmap)
        painter.drawPixmap(point,pixmap)

    def ChangePixmap(self, img):
        self.im = Image.open(str(img))
        self.im.thumbnail(self.size)
        self.repaint()  # repaint() will trigger the paintEvent(self, event), this way the new pixmap will be drawn on the label

class ImageLabel2(QLabel):
    def __init__(self):
        super(ImageLabel2, self).__init__()
        self.setAlignment(Qt.AlignLeft)
        self.setAlignment(Qt.AlignTop)
        self.setMaximumHeight(480)
        self.setMinimumHeight(480)
        self.setMaximumWidth(640)
        self.setFixedWidth(640)
        self.setFrameStyle(QFrame.StyledPanel)
        self.showImageByPath("images\\python.png")

    def showImageByPath(self, path):

        if path:
            image = QImage(path)
            pp = QPixmap.fromImage(image)
            pixmapHeight = pp.height()
            labelHeight = self.height()
            if pixmapHeight < labelHeight:
                scalingFactor = float(pixmapHeight) / labelHeight
            else:
                scalingFactor = 1.0
            print(" Scaling factor = %f", scalingFactor)
            self.setPixmap(pp.scaled(
                self.size()*scalingFactor,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation))
            self.show()

class MyButton(QPushButton):
    def __init__(self, text):
        super(MyButton, self).__init__()
        self.setFixedWidth(120)
        self.setFixedHeight(30)
        self.setFont(QFont('SansSerif', 10))
        self.setStyleSheet("background-color: #FFF096; color: blue")
        # self.setStyleSheet("color: blue")
        self.setText(text)
    def close(self):
        self

    def deleteImageTable(self):
        global myBrowser
        myBrowser.clearTable()

    def InsertARow(self):
        global myBrowser
        myBrowser.model.insertRow(0, "testing ")
