import sys
import MyWidgets
import os

import pyqtgraph as pg
import numpy as np

from PyQt5 import uic
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QT_VERSION_STR, QPoint, QDir, QEvent

from PyQt5.QtGui import QImage, QPixmap, QPainterPath, QPainter, QFont, QIcon, QPalette, QColor, QLinearGradient

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QGridLayout, QVBoxLayout, QMainWindow, QAction, QTableView, QTabWidget, QMessageBox, \
    QComboBox, QStyleFactory, QCheckBox, QFileDialog

class MyButton(QPushButton):
    def __init__(self, text):
        super(MyButton, self).__init__()
        self.setFixedWidth(100)
        self.setFixedHeight(20)
        self.setFont(QFont('SansSerif', 8))
        self.setStyleSheet("background-color: #FFF096; color: blue; border-style: inset; border-width: 1px; border-radius: 5px;  padding:4px;")
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

class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()

        # self.ui = uic.loadUi('GameOfLife.ui', self)
        # self.ui.actionQuit.triggered.connect(self.close_application)

        # +++++++++++++++++++++++++++++++++++++++++++++
        # Create Toolbar
        # +++++++++++++++++++++++++++++++++++++++++++++
        self.actionQuit = QAction(QIcon('icons/exit.png'), 'Close the application', self)
        self.actionQuit.triggered.connect(self.close_application)
        self.toolBar = self.addToolBar("GameOfLifeToolbar")
        self.toolBar.addAction(self.actionQuit)

        # +++++++++++++++++++++++++++++++++++++++++++++
        # Create Layouts
        # +++++++++++++++++++++++++++++++++++++++++++++
        self.topLevelLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.auxInfoLayout = QVBoxLayout()
        self.panelLayout = QHBoxLayout()

        self.buttonLayout.setAlignment(Qt.AlignLeft)

        # +++++++++++++++++++++++++++++++++++++++++++++
        # Create Buttons
        # +++++++++++++++++++++++++++++++++++++++++++++
        self.clearButton = QPushButton("Clear")
        self.startStopButton = MyButton("Start")
        self.randomFillButton = MyButton("Random Fill")
        self.SavePathButton = MyWidgets.LabelledButton("Save To...")

        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        # Connect the controls to handlers
        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.clearButton.clicked.connect(self.clearGrid)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        # Add buttons to the button bar
        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.buttonLayout.addWidget(self.clearButton)
        self.buttonLayout.addWidget(self.startStopButton)
        self.buttonLayout.addWidget(self.randomFillButton)
        self.buttonLayout.addWidget(self.SavePathButton)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        # Create the main grid view
        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.mainGridView = pg.GraphicsLayoutWidget()
        self.mainGridView.setFixedWidth(500)
        self.mainGridView.setFixedHeight(500)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        # Create the timing graph view
        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.timingGraphView = pg.GraphicsLayoutWidget()
        self.timingGraphView.setFixedWidth(500)
        self.timingGraphView.setFixedHeight(200)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        # Create the debug info view
        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.debugInfo = QTextEdit()
        self.debugInfo.setFixedWidth(500)
        self.debugInfo.setFixedHeight(300)
        self.debugInfo.setText("Debug info goes here....")

        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        # Add the timing graph and debug info into their layout
        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.auxInfoLayout.addWidget(self.timingGraphView)
        self.auxInfoLayout.addWidget(self.debugInfo)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        # Add the main grid and aux info into a horizontal layout
        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.panelLayout.addWidget(self.mainGridView)
        self.panelLayout.addLayout(self.auxInfoLayout)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        # Add everything into the top level layout
        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.topLevelLayout.addLayout(self.panelLayout)
        self.topLevelLayout.addLayout(self.buttonLayout)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.topLevelLayout)

        self.setCentralWidget(self.mainWidget)

        self.gfx = self.mainGridView.addPlot()
        # self.gfx = self.ui.graphicsView.addPlot()
        self.restartPlot()



    def restartPlot(self):
        self.mainGridView.removeItem(self.gfx)
        self.gfx = self.mainGridView.addPlot()
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

    def clearGrid(self):
        print("Clearing the grid now...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GameOfLifeMainWin = MainWin()
    GameOfLifeMainWin.show()
sys.exit(app.exec_())
