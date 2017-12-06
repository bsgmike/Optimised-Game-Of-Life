import sys, random
from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QGridLayout, QVBoxLayout, QMainWindow, QFontComboBox, QPlainTextEdit

from PyQt5.QtGui import QFont, QColor

from PyQt5.QtCore import QRect, QPoint

# ++++++++++++++++++++++++++++++++++++++++++++++
#          GLOBALS
# ++++++++++++++++++++++++++++++++++++++++++++++
tileColors = ["red", "black", "blue", "yellow"]
tileOwner = ["player", "board", "bag"]
tileValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


class DragLabel(QLabel):
    def __init__(self, color, text, parent):
        super(DragLabel, self).__init__(parent)
        widthText = "13"
        tileFont = QFont("Consolas", 10)
        self.setFont(tileFont)
        metric = QtGui.QFontMetrics(self.font())
        size = metric.size(QtCore.Qt.TextSingleLine, widthText)

        image = QtGui.QImage(size.width() + 12, size.height() + 22,
                             QtGui.QImage.Format_ARGB32_Premultiplied)

        # image = QtGui.QImage(self.width, self.height, QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtGui.qRgba(0, 0, 0, 0))

        # font = QtGui.QFont()
        # font.setStyleStrategy(QtGui.QFont.ForceOutline)

        painter = QtGui.QPainter()
        painter.begin(image)
        if color == "red":
            painter.setBrush(QtCore.Qt.red)
            painter.setPen(QtCore.Qt.red)
        elif color == "blue":
            painter.setBrush(QtCore.Qt.blue)
            painter.setPen(QtCore.Qt.blue)
        elif color == "yellow":
            painter.setBrush(QtCore.Qt.yellow)
            painter.setPen(QtCore.Qt.yellow)
        else:
            painter.setBrush(QtCore.Qt.black)
            painter.setPen(QtCore.Qt.black)

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        # painter.setBrush(QtCore.Qt.white)
        painter.setBrush(QColor('#999999'))
        painter.drawRoundedRect(QtCore.QRectF(0.5, 0.5, image.width() - 1,
                                              image.height() - 4), 30, 30, QtCore.Qt.RelativeSize)

        painter.setFont(tileFont)

        painter.setBrush(QtCore.Qt.blue)

        painter.drawText(QRect(QPoint(6, 6), size), QtCore.Qt.AlignCenter, text)
        painter.end()

        self.setPixmap(QtGui.QPixmap.fromImage(image))
        self.labelText = text


class RummyTile(QWidget):
    def __init__(self, color, value):
        super(RummyTile, self).__init__()
        self.tileLabel = DragLabel(color, str(value), self)

        self.color = color
        self.value = value
        self.owner = "bag"
        self.setObjectName("rummyTile")
        self.cellListIndex = 0
        self.labelText = "hello world"

    def mousePressEvent(self, event):
        # itemData = QtCore.QByteArray()
        # dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        # dataStream << QtCore.QByteArray(self.labelText) << QtCore.QPoint(event.pos() - self.rect().topLeft())
        #
        mimeData = QtCore.QMimeData()
        mimeData.setText("hello world")
        # mimeData.setData('application/x-fridgemagnet', 0)
        # mimeData.setText(self.cellListIndex)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - self.rect().topLeft())
        drag.setPixmap(self.tileLabel.pixmap())
        gameBoard.setStartCellIndex(self.cellListIndex)
        gameBoard.removeTile(self.cellListIndex)
        self.hide()

        if drag.exec_(QtCore.Qt.MoveAction | QtCore.Qt.CopyAction, QtCore.Qt.CopyAction) == QtCore.Qt.MoveAction:
            self.close()
        else:
            self.show()

    def getColor(self):
        return self.color

    def getValue(self):
        return self.value

    def setCellListIndex(self, listIndex):
        self.cellListIndex = listIndex

    def getCellListIndex(self, listIndex):
        return self.cellListIndex

    def __str__(self):
        myStr = ""
        if self.tileBag == []:
            return "bag is empty"
        else:
            return "Here's the tile bag"
            # for tile in self.tileBag:
            #     myStr += tile.getColor() + "  " + str(tile.getValue()) + "\n"
            #  # return '<%s => %s>' % (self.__class__.__name__, self.name)
            # return myStr

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
        self.setFrameStyle(QFrame.Box)
        self.layout = QVBoxLayout()
        # self.layout.setContentsMargins(left, top, right, bottom)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.setLayout(self.layout)
        self.setFixedHeight(48)
        self.setFixedWidth(38)
        self.row = row
        self.col = col
        self.cellListIndex = 0

        pal = self.palette()
        pal.setColor(self.backgroundRole(), QColor('#888844'))
        pal.setColor(self.foregroundRole(), QColor('#999955'))  # 6600cc
        self.setPalette(pal)
        self.setAutoFillBackground(True)

        self.setMouseTracking(True)
        self.setAcceptDrops(True)
        self.residentTile = []

    def setCellListIndex(self, listIndex):
        self.cellListIndex = listIndex

    def getCellListIndex(self):
        return self.cellListIndex

    def mousePressEvent(self, QMouseEvent):
        print(QMouseEvent.pos())
        self.getCellStatus()

    def enterEvent(self, a0: QtCore.QEvent):
        print("Mouse entered", self.row, self.col)
        self.getCellStatus()

    def addTile(self, newTile):
        self.residentTile = [newTile.getColor(), newTile.getValue()]
        self.layout.addWidget(newTile)

    def getResidentTileValue(self):
        return self.residentTile

    def removeTile(self):
        print("Remove tile in cell ", str(self.cellListIndex))
        cellContents = self.findChild(RummyTile)
        if cellContents != None:
            while self.layout.count():
                child = self.layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        self.getCellStatus()


    def getCellStatus(self):
        cellContents = self.findChild(RummyTile)

        if cellContents == None:
            print("Cell Status: cell ", str(self.cellListIndex), " is empty")
            return "Empty"
        else:
            print("Cell Status::-", str(self.cellListIndex), " contains ", cellContents.color, cellContents.value)
            return cellContents.color, cellContents.value

    def getPosition(self):
        return self.row, self.col

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-fridgemagnet'):
            if event.source() in self.children():
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        elif event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    dragMoveEvent = dragEnterEvent

    def dropEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            mime = event.mimeData()
            sourceIndex = gameBoard.getStartCellIndex()
            if self.residentTile != []:
                # the cell we are dropping onto already contains a tile. So we want to put this tile into
                # the cell where the drag started. Thereby swapping the tiles
                newTile = RummyTile(self.residentTile[0], self.residentTile[1])
                gameBoard.cellList[sourceIndex].addTile(newTile)


            # newLabel = RummyTile.DragLabel(text, self)

            sourceTileValue = gameBoard.cellList[sourceIndex].getResidentTileValue()
            newTile = RummyTile(sourceTileValue[0], sourceTileValue[1])
            newTile.setCellListIndex(self.cellListIndex)
            # gameBoard.cellList[gameBoard.getStartCellIndex()].removeTile()
            self.layout.addWidget(newTile)


            if event.source() in self.children():
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        elif event.mimeData().hasText():
            pieces = event.mimeData().text().split()
            position = event.pos()

            for piece in pieces:
                newLabel = RummyTile.DragLabel(piece, self)
                newLabel.move(position)
                newLabel.show()

                position += QtCore.QPoint(newLabel.width(), 0)

            event.acceptProposedAction()
        else:
            event.ignore()

class GameBoard(QFrame):
    def __init__(self):
        super(GameBoard, self).__init__()
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.tileGrid = QGridLayout()
        self.tileGrid.setHorizontalSpacing(0)
        self.tileGrid.setVerticalSpacing(0)
        self.rows = 8
        self.cols = 30
        self.cellList = []
        self.startCellIndex = 0 #the index of the cell from where the drag started

        pal = self.palette()
        pal.setColor(self.backgroundRole(), QColor('#888844'))
        pal.setColor(self.foregroundRole(), QColor('#888844'))  # 6600cc
        self.setPalette(pal)
        self.setAutoFillBackground(True)

        for row in range(self.rows):
            for col in range(self.cols):
                newCell = BoardCell(row, col)
                newCell.setCellListIndex(len(self.cellList))
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
                cellIndex = cell.getCellListIndex()
                tile.setCellListIndex(cellIndex)
                cell.addTile(tile)
                break

    def GetNextEmptyCellPosition(self):
        print("GetNextEmptyCellPosition")

    def setStartCellIndex(self, val):
        self.startCellIndex = val

    def removeTile(self, index):
        self.cellList[index].removeTile()

    def getStartCellIndex(self):
        return self.startCellIndex


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