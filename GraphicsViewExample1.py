# simple code by Krystian Samp - krychu (samp[dot]krystian[monkey]gmail.com), November 2006

import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QApplication

class MyView(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)

        self.scene = QGraphicsScene(self)
        self.item = QGraphicsEllipseItem(-20, -10, 40, 20)
        self.scene.addItem(self.item)
        self.setScene(self.scene)

        # Remember to hold the references to QTimeLine and QGraphicsItemAnimation instances.
        #  They are not kept anywhere, even if you invoke QTimeLine.start().
        self.tl = QtCore.QTimeLine(1000)
        self.tl.setFrameRange(0, 100)
        self.a = QPropertyAnimation()
        self.a.setTargetObject(self.item)
        # self.a.setItem(self.item)
        self.a.setTimeLine(self.tl)

        # Each method determining an animation state (e.g. setPosAt, setRotationAt etc.)
        # takes as a first argument a step which is a value between 0 (the beginning of the
        # animation) and 1 (the end of the animation)
        self.a.setPosAt(0, QtCore.QPointF(0, -10))
        self.a.setRotationAt(1, 360)

        self.tl.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MyView()
    view.show()
    sys.exit(app.exec_())