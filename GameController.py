import sys
import MyWidgets
import os
import GridType1
import pyqtgraph as pg
import numpy as np

from PyQt5 import uic
from PyQt5.QtCore import Qt

from PyQt5.QtGui import  QFont, QIcon, QPalette, QColor, QLinearGradient

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QHBoxLayout, QVBoxLayout, QMainWindow, QAction


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
        self.columnSize = 40
        self.rowSize = self.columnSize
        self.xInitPos = 0
        self.yInitPos = 0
        self.state = GridType1.gridType1(self.rowSize, self.columnSize)
        self.dataPlot = pg.ScatterPlotItem()
        self.pause = True
        self.generation = 0
        self.color1 = pg.mkBrush("#E8DB9A")
        self.color2 = pg.mkBrush("#132DFF")
        self.brushes = []
        self.cells = []
        self.alive = 0

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
        self.startStopButton = QPushButton("Start")
        self.randomFillButton = QPushButton("Random Fill")
        # self.SavePathButton = MyWidgets.LabelledButton("Save To...")
        self.generationCountLabel = MyWidgets.InformationLabel("Generation Count")
        self.generationCountLabel.updateText(str(self.generation))

        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        # Connect the controls to handlers
        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.clearButton.clicked.connect(self.clearGrid)
        self.startStopButton.clicked.connect(self.startPause)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        # Add buttons to the button bar
        # ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.buttonLayout.addWidget(self.clearButton)
        self.buttonLayout.addWidget(self.startStopButton)
        self.buttonLayout.addWidget(self.randomFillButton)
        self.buttonLayout.addWidget(self.generationCountLabel)
        # self.buttonLayout.addWidget(self.SavePathButton)

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
        self.restartPlot()
        self.createGrid()
        self.updateGrid()

        # Generation Timer
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.TIME_INTERVAL = 100
        self.TIME_INTERVAL_MAX = 200

    def restartPlot(self):
        self.mainGridView.removeItem(self.gfx)
        self.gfx = self.mainGridView.addPlot()
        self.dataPlot = pg.ScatterPlotItem()
        self.gfx.addItem(self.dataPlot)
        self.gfx.hideAxis('bottom')
        self.gfx.hideAxis('left')
        self.gfx.setXRange(1, 0)
        self.gfx.setYRange(1, 0)
        self.gfx.setMouseEnabled(x=False, y=False)
        self.gfx.enableAutoRange(x=True, y=True)

    def updateTimer(self):
        if self.pause == False:
            self.nextState()
            self.timer.start(self.TIME_INTERVAL)

    def close_application(self):
        print("Exiting now...")
        sys.exit()

    def clearGrid(self):
        print("Clearing the grid now...")

    def startPause(self):
        if self.pause:
            self.pause = False
            self.updateTimer()
            print("start")
        else:
            self.pause = True
            print("stop")

    def nextState(self):
        self.state.tick()
        self.updateGrid()
        linea = '# Generacion: '+str(self.generation)+'     # Celdas Vivas: '+str(self.alive)
        # self.ui.infoBox.append(linea)
        # self.aliveEvolution.append(self.alive)
        # self.restartPlot2()
        self.generation += 1
        self.generationCountLabel.updateText(str(self.generation))

    def clicked(self, plot, points):
        x, y = points[0].pos()
        x = int(x - 0.5)
        y = int(y - 1.5)
        print("cell selected: pos= ", x, " : ", y, "\n")
        if self.state.prevState[self.rowSize - 1 - y, x] == 1:
            self.state.prevState[self.rowSize - 1 - y, x] = 0
        else:
            self.state.prevState[self.rowSize - 1 - y, x] = 1
        self.updateGrid()

    def createGrid(self):
        self.pause = True
        self.generation = 0
        self.cells = []
        self.brushes = []
        self.dataPlot.clear()
        self.state = GridType1.gridType1(self.rowSize, self.columnSize)

        for i in range(self.rowSize):
            for j in range(self.columnSize):
                if self.state.prevState[i, j] == 0:
                    self.brushes.append(self.color1)
                else:
                    self.brushes.append(self.color2)
                self.cells.append({'pos': (j + 0.5, self.rowSize - i + 0.5),
                                   'size': 500 / self.rowSize,
                                   'symbol': 's',
                                   'brush': self.brushes[-1],
                                   'pen': {'color': (0, 0, 0),
                                           'width': 0.5},
                                   })

        self.dataPlot.addPoints(self.cells)
        self.dataPlot.sigClicked.connect(self.clicked)

    def updateGrid(self):
        ctr = 0
        self.alive = 0
        for i in range(self.rowSize):
            for j in range(self.columnSize):
                if self.state.prevState[i,j] == 0:
                    self.brushes[ctr] = self.color1
                else:
                    self.brushes[ctr] = self.color2
                    self.alive += 1
                ctr += 1
        self.dataPlot.setBrush(self.brushes, mask=None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    GameOfLifeMainWin = MainWin()
    GameOfLifeMainWin.show()
sys.exit(app.exec_())
