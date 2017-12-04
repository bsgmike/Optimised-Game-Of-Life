import sys, random
from PyQt5 import QtGui, QtCore
from RummyTile import RummyTile
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QGridLayout, QVBoxLayout, QMainWindow, QFontComboBox, QPlainTextEdit

from PyQt5.QtGui import QFont

from PyQt5.QtCore import QRect, QPoint

# ++++++++++++++++++++++++++++++++++++++++++++++
#          GLOBALS
# ++++++++++++++++++++++++++++++++++++++++++++++
tileColors = ["red", "black", "blue", "yellow"]
tileOwner = ["player", "board", "bag"]
tileValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()

        # ++++++++++++++++++++++++++++++++++++++++++++++++
        # Create all the game board sections
        # ++++++++++++++++++++++++++++++++++++++++++++++++
        self.player1Grid = PlayerGrid()
        self.player2Grid = PlayerGrid()
        # self.controlPanel = ControlPanel()

        # ++++++++++++++++++++++++++++++++++++++++++++++++
        # Add everything to the grid layout
        # ++++++++++++++++++++++++++++++++++++++++++++++++
        self.gameLayout = QGridLayout()
        self.gameLayout.addWidget(self.player1Grid, 0, 0)
        self.gameLayout.addWidget(gameBoard, 1, 0, 3, 1)
        self.gameLayout.addWidget(self.player2Grid, 4, 0)
        self.gameLayout.addWidget(controlPanel, 0, 1, 5 ,1)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.gameLayout)

        self.setCentralWidget(self.mainWidget)

        self.setGeometry(200, 200, 850, 500)


class ControlPanel(QFrame):
    def __init__(self):
        super(ControlPanel, self).__init__()
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.layout = QVBoxLayout()
        self.layout.setAlignment((QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop))
        self.setLayout(self.layout)
        self.setMinimumHeight(600)
        self.setMinimumWidth(200)
        self.buttonBar = QVBoxLayout()

        # ++++++++++++++++++++++++++++++++++++++++++++++++
        # Create buttons
        # ++++++++++++++++++++++++++++++++++++++++++++++++
        self.addTileButton = QPushButton("Take Tile")
        self.addTileButton.clicked.connect(self.takeTile)

        self.addExitButton = QPushButton("Exit")
        self.addExitButton.clicked.connect(self.Exit)

        self.buttonBar.addWidget(self.addTileButton)
        self.buttonBar.addWidget(self.addExitButton)

        self.layout.addLayout(self.buttonBar)
        self.infoBar = QVBoxLayout()
        self.layout.setAlignment((QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop))

        # ++++++++++++++++++++++++++++++++++++++++++++++++
        # Create info box
        # ++++++++++++++++++++++++++++++++++++++++++++++++
        self.tilesLeftInfoBox = QPlainTextEdit()
        tileLeftFont = QFont("Consolas", 10)
        self.tilesLeftInfoBox.setFont(tileLeftFont)
        self.tilesLeftInfoBox.setPlainText("All tiles in bag")
        self.infoBar.addWidget(self.tilesLeftInfoBox)
        self.layout.addLayout(self.infoBar)



    def takeTile(self):
        print("Taking a tile")
        if tileBag.getNoOfTilesInBag() > 0:
            nextTile = tileBag.getTileFromBag()
            gameBoard.AddTileFromBag(nextTile)


    def Exit(self):
        print("Exiting....")
        sys.exit()

    def setNumberOfTiles(self, NoOfTiles):
        tempStr = str(NoOfTiles) + " tiles left in bag"
        self.tilesLeftInfoBox.setPlainText(tempStr)



class BoardCell(QFrame):
    def __init__(self, row, col):
        super(BoardCell, self).__init__()
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.layout = QVBoxLayout()
        # self.layout.setContentsMargins(left, top, right, bottom)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.setLayout(self.layout)
        # self.setMinimumHeight(48)
        # self.setMinimumWidth(38)
        self.setFixedHeight(48)
        self.setFixedWidth(38)
        self.row = row
        self.col = col

        self.setMouseTracking(True)

    def mousePressEvent(self, QMouseEvent):
        print(QMouseEvent.pos())
        self.getCellStatus()

    def enterEvent(self, a0: QtCore.QEvent):
        print("Mouse entered", self.row, self.col)
        self.getCellStatus()

    def addTile(self, RummyTile):
        self.layout.addWidget(RummyTile)

    def removeTile(self, RummyTile):
        self.layout.removeWidget(RummyTile)

    def getCellStatus(self):
        cellContents = self.findChild(RummyTile)

        if cellContents == None:
            print("Cell Status: this cell is empty")
            return "Empty"
        else:
            print("Cell Status::-", cellContents.color, cellContents.value)
            return cellContents.color, cellContents.value

    def getPosition(self):
        return self.row, self.col

class GameBoard(QFrame):
    def __init__(self):
        super(GameBoard, self).__init__()
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.tileGrid = QGridLayout()
        self.tileGrid.setHorizontalSpacing(4)
        self.tileGrid.setVerticalSpacing(4)
        self.rows = 8
        self.cols = 30
        self.cellList = []

        for row in range(self.rows):
            for col in range(self.cols):
                newCell = BoardCell(row, col)
                self.tileGrid.addWidget(newCell, row, col)  # i=row j=col
                self.cellList.append(newCell)


        # for tileColor in tileColors:
        #     for tileVal in tileValues:
        #         newCell = BoardCell(row, col)
        #         newCell.addTile(RummyTile(tileColor, tileVal))
        #         self.tileGrid.addWidget(newCell, row, col)  # i=row j=col
        #         col = col + 1
        #     row = row + 1
        #     col = 0

        # for n in range(10):
        #     newCell = BoardCell(row, col)
        #     newCell.addTile(tileBag.getTileFromBag())
        #     self.tileGrid.addWidget(newCell, row, col)
        #     col += 1

        self.setLayout(self.tileGrid)
        self.listItems()

    def listItems(self):
        print("List grid contents")
        cellsList = self.findChildren(BoardCell)
        for cell in cellsList:
            print(cell.row, cell.col)

    def AddTileFromBag(self, tile):
        print("AddTileFromBag")
        # take a tile from the bag and put it in the
        # next empty cell
        # go through the cell list calling getStatus(). The first
        # cell that returns empty is the one to add the tile to
        for cell in self.cellList:
            status = cell.getCellStatus()
            if status == "Empty":
                cell.addTile(tile)
                break

    def GetNextEmptyCellPosition(self):
        print("GetNextEmptyCellPosition")


class PlayerGrid(QFrame):
    def __init__(self):
        super(PlayerGrid, self).__init__()
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        QRect = self.contentsRect()

        self.tileGrid = QGridLayout()

        self.setLayout(self.tileGrid)

class TileBag():
    def __init__(self):
        self.tileBag = []
        self.nextTileToDeal = 0
        for tileColor in tileColors:
            for tileVal in tileValues:
                self.tileBag.append(RummyTile(tileColor, tileVal))
        random.shuffle(self.tileBag)
        print("finished filling tile bag")

    def getTileFromBag(self):
        # global controlPanel
        # if self.nextTileToDeal == len(self.tileBag):
        #     return("No Tiles Left")
        # else:
        #     print("get tile:- ", self.tileBag[self.nextTileToDeal].color, self.tileBag[self.nextTileToDeal].value)
        #     self.nextTileToDeal += 1
        #     return self.tileBag[self.nextTileToDeal]
        if self.tileBag == []:
            return "empty"
        else:
            tile = self.tileBag.pop()
            controlPanel.setNumberOfTiles(len(self.tileBag) - 1)
            return tile

    def getNoOfTilesInBag(self):
        return len(self.tileBag) - 1

class FontSelector(QWidget):
    def __init__(self):
        super(FontSelector, self).__init__()
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout = QHBoxLayout(self.frame)

        self.textBold = QPushButton(self.frame)
        self.textBold.setMaximumSize(QtCore.QSize(25, 25))
        self.textBold.setCheckable(True)
        self.textBold.setText("B")
        self.horizontalLayout.addWidget(self.textBold)

        self.textItalic = QPushButton(self.frame)
        self.textItalic.setMaximumSize(QtCore.QSize(25, 25))
        self.textItalic.setCheckable(True)
        self.textItalic.setText("I")
        self.horizontalLayout.addWidget(self.textItalic)

        self.textUnderline = QPushButton(self.frame)
        self.textUnderline.setMaximumSize(QtCore.QSize(25, 25))
        self.textUnderline.setCheckable(True)
        self.textUnderline.setText("U")
        self.horizontalLayout.addWidget(self.textUnderline)

        self.fontComboBox = QFontComboBox(self.frame)
        self.horizontalLayout.addWidget(self.fontComboBox)
        self.setLayout(self.horizontalLayout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tileBag = TileBag()
    gameBoard = GameBoard()
    controlPanel = ControlPanel()

    RummyKub = MainWin()
    RummyKub.show()
sys.exit(app.exec_())