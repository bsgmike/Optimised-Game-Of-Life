import sys
from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QGridLayout, QVBoxLayout, QMainWindow, QAction, QTableView, QTabWidget, QMessageBox, \
    QComboBox, QStyleFactory, QCheckBox, QFileDialog, QFontComboBox

from PyQt5.QtGui import QFont

from PyQt5.QtCore import QRect, QPoint


# ++++++++++++++++++++++++++++++++++++++++++++++
#          GLOBALS
# ++++++++++++++++++++++++++++++++++++++++++++++
tileColors = ["red", "black", "blue", "yellow"]
tileValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

class DragLabel(QLabel):
    def __init__(self, text, parent):
        super(DragLabel, self).__init__(parent)

        tileFont = QFont("Consolas", 10)
        self.setFont(tileFont)
        metric = QtGui.QFontMetrics(self.font())
        size = metric.size(QtCore.Qt.TextSingleLine, text)

        self.width = 30
        self.height = 40

        image = QtGui.QImage(size.width() + 12, size.height() + 12,
                QtGui.QImage.Format_ARGB32_Premultiplied)

        # image = QtGui.QImage(self.width, self.height, QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtGui.qRgba(0, 0, 0, 0))

        # font = QtGui.QFont()
        # font.setStyleStrategy(QtGui.QFont.ForceOutline)

        painter = QtGui.QPainter()
        painter.begin(image)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtCore.Qt.white)
        painter.drawRoundedRect(QtCore.QRectF(0.5, 0.5, image.width()-1,
                image.height()-1), 25, 25, QtCore.Qt.RelativeSize)

        painter.setFont(tileFont)
        painter.setBrush(QtCore.Qt.black)

        painter.drawText(QRect(QPoint(6, 6), size), QtCore.Qt.AlignCenter, text)
        painter.end()

        self.setPixmap(QtGui.QPixmap.fromImage(image))
        self.labelText = text

    def mousePressEvent(self, event):
        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        dataStream << QtCore.QByteArray(self.labelText) << QtCore.QPoint(event.pos() - self.rect().topLeft())

        mimeData = QtCore.QMimeData()
        mimeData.setData('application/x-fridgemagnet', itemData)
        mimeData.setText(self.labelText)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - self.rect().topLeft())
        drag.setPixmap(self.pixmap())

        self.hide()

        if drag.exec_(QtCore.Qt.MoveAction | QtCore.Qt.CopyAction, QtCore.Qt.CopyAction) == QtCore.Qt.MoveAction:
            self.close()
        else:
            self.show()

class RummyTile(QWidget):
    def __init__(self, value):
        super(RummyTile, self).__init__()

        dictionaryFile = QtCore.QFile(':/dictionary/words.txt')
        dictionaryFile.open(QtCore.QFile.ReadOnly)

        x = 5
        y = 5

        self.tileLabel = DragLabel(str(value), self)
        self.show()

        # # for word in QtCore.QTextStream(dictionaryFile).readAll().split():
        # #     wordLabel = DragLabel(word, self)
        # #     wordLabel.move(x, y)
        # #     wordLabel.show()
        # #     x += wordLabel.width() + 2
        # #     if x >= 245:
        # #         x = 5
        # #         y += wordLabel.height() + 2
        #
        # newPalette = self.palette()
        # newPalette.setColor(QtGui.QPalette.Window, QtCore.Qt.white)
        # self.setPalette(newPalette)
        #
        # self.setMinimumSize(400, max(200, y))
        # self.setWindowTitle("Fridge Magnets")
        self.setAcceptDrops(True)

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
        if event.mimeData().hasFormat('application/x-fridgemagnet'):
            mime = event.mimeData()
            itemData = mime.data('application/x-fridgemagnet')
            dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.ReadOnly)

            text = QtCore.QByteArray()
            offset = QtCore.QPoint()
            dataStream >> text >> offset

            try:
                # Python v3.
                text = str(text, encoding='latin1')
            except TypeError:
                # Python v2.
                text = str(text)

            newLabel = DragLabel(text, self)
            newLabel.move(event.pos() - offset)
            newLabel.show()

            if event.source() in self.children():
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        elif event.mimeData().hasText():
            pieces = event.mimeData().text().split()
            position = event.pos()

            for piece in pieces:
                newLabel = DragLabel(piece, self)
                newLabel.move(position)
                newLabel.show()

                position += QtCore.QPoint(newLabel.width(), 0)

            event.acceptProposedAction()
        else:
            event.ignore()

class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        self.gameBoard = GameBoard()
        self.player1Grid = PlayerGrid()
        self.player2Grid = PlayerGrid()

        self.gameLayout = QGridLayout()

        self.gameLayout.addWidget(self.player1Grid, 0, 0)
        self.gameLayout.addWidget(self.gameBoard, 1, 0, 3, 1)
        self.gameLayout.addWidget(self.player2Grid, 5, 0)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.gameLayout)

        self.setCentralWidget(self.mainWidget)

        self.setGeometry(200, 200, 850, 500)


class BoardCell(QFrame):
    def __init__(self, row, col):
        super(BoardCell, self).__init__()
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.layout = QVBoxLayout()
        # self.layout.setContentsMargins(left, top, right, bottom)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.setLayout(self.layout)
        self.setMinimumHeight(40)
        self.setMinimumWidth(30)
        self.row = row
        self.col = col

        self.setMouseTracking(True)

    def enterEvent(self, a0: QtCore.QEvent):
        print("Mouse entered", self.row, self.col)

    def addTile(self, RummyTile):
        self.layout.addWidget(RummyTile)




class GameBoard(QFrame):
    def __init__(self):
        super(GameBoard, self).__init__()
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.tileGrid = QGridLayout()
        self.rows = 6
        self.cols = 25
        row = 0
        col = 0
        for tileColor in tileColors:
            for tileVal in tileValues:
                newCell = BoardCell(row, col)
                newCell.addTile(RummyTile(tileVal))
                self.tileGrid.addWidget(newCell, row, col)  # i=row j=col
                col = col + 1
            row = row + 1
            col = 0


        # for i in range(1, self.rows):
        #     for j in range(1, self.cols):
        #         newCell = BoardCell(i,j)
        #         newCell.addTile(RummyTile(0))
        #         self.tileGrid.addWidget(newCell, i, j) #i=row j=col

        self.setLayout(self.tileGrid)
        self.listItems()




    def listItems(self):
        print("List grid contents")
        cellsList = self.findChildren(BoardCell)
        for cell in cellsList:
            print(cell.row, cell.col)


class PlayerGrid(QFrame):
    def __init__(self):
        super(PlayerGrid, self).__init__()
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)



        QRect = self.contentsRect()

        self.tileGrid = QGridLayout()


        self.setLayout(self.tileGrid)

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
    GameOfLifeMainWin = MainWin()
    GameOfLifeMainWin.show()
sys.exit(app.exec_())