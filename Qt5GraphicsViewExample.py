from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QT_VERSION_STR, QPoint, QDir, QEvent

from PyQt5.QtGui import QImage, QPixmap, QPainterPath, QPainter, QFont, QIcon, QPalette, QColor, QLinearGradient

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTreeView, QFileSystemModel, QLineEdit, \
    QLabel, QFrame, QTextEdit, QHBoxLayout, QVBoxLayout, QMainWindow, QAction, QTableView, QTabWidget, QMessageBox, \
    QComboBox, QStyleFactory, QCheckBox, QFileDialog

import sys
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsTextItem, QApplication, QGraphicsItem


class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        self.qt_test()

    def qt_test(self):
        """
        Test that Qt actually works
        """
        self.scene = QGraphicsScene(self)
        self.scene.addText("Hello, world!nmnmn")
        # text = QGraphicsTextItem(self, None)
        # text.setHtml("<h2 align=\"center\">hello</h2><h2 align=\"center\">world 12334345354444444444444444444444444</h2>123");
        # text.setPos(QPointF(25,25))
        self.greenBrush = QBrush(QColor(Qt.green))
        self.blueBrush = QBrush(QColor(Qt.blue))

        self.outlinePen = QPen(QColor(Qt.red))
        self.outlinePen.setWidth(2);

        self.greenRect = self.scene.addRect(100, 0, 80, 100, self.outlinePen, self.greenBrush)
        self.greenRect.setFlag(QGraphicsItem.ItemIsMovable)
        self.blueRect = self.scene.addRect(100, 0, 80, 100, self.outlinePen, self.blueBrush)
        self.blueRect.setFlag(QGraphicsItem.ItemIsMovable)
        self.view = QGraphicsView(self.scene)
        self.view.setFixedSize(800, 600)
        self.view.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GameOfLifeMainWin = MainWin()
    # GameOfLifeMainWin.show()
sys.exit(app.exec_())



# app = QApplication([])
#
# scene = QGraphicsScene()
# scene.addText("Hello, world!")
# view = QGraphicsView(scene)
# view.show()

app.exec_()