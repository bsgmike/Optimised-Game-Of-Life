import sys
import os

import pyqtgraph as pg
import numpy as np

from PyQt5 import uic
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QT_VERSION_STR, QPoint, QDir, QEvent

from PyQt5.QtGui import QImage, QPixmap, QPainterPath, QPainter, QFont, QIcon, QPalette, QColor, QLinearGradient

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QVBoxLayout, QMainWindow, QAction, QTableView, QTabWidget, QMessageBox, \
    QComboBox, QStyleFactory, QCheckBox, QFileDialog


class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()

        self.ui = uic.loadUi('GameOfLife.ui', self)
        self.ui.actionQuit.triggered.connect(self.close_application)

        self.gfx = self.ui.graphicsView.addPlot()
        self.restartPlot()



    def restartPlot(self):

        self.ui.graphicsView.removeItem(self.gfx)
        self.gfx = self.ui.graphicsView.addPlot()
        self.datos = pg.ScatterPlotItem()
        self.gfx.addItem(self.datos)
        self.gfx.hideAxis('bottom')
        self.gfx.hideAxis('left')
        self.gfx.setXRange(1,0)
        self.gfx.setYRange(1,0)
        self.gfx.setMouseEnabled(x=False, y=False)
        self.gfx.enableAutoRange(x=True,y=True)

    def close_application(self):
        print("Exiting now...")
        sys.exit()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    GameOfLifeMainWin = MainWin()
    GameOfLifeMainWin.show()
sys.exit(app.exec_())
