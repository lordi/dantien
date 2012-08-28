from PyQt4 import QtGui, QtCore
import numpy as np
from qimage2ndarray import array2qimage

class Spectrogram (QtGui.QWidget):
    def __init__(self, parent, model):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 250, 150)
        self.model = model
        self.text = u''

    def paintEvent(self, event):
        paint = QtGui.QPainter()
        paint.begin(self)
        paint.setPen(QtGui.QColor(168, 34, 3))
        paint.setFont(QtGui.QFont('Decorative', 10))
        paint.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)
        paint.drawImage(0,0,array2qimage(self.model.dat_s, True))
        paint.end()

class Dantien(QtGui.QMainWindow):
    ''' Dantien main window '''

    def __init__(self, model):
        QtGui.QMainWindow.__init__(self)

        self.model = model

        widget = Spectrogram(self, model)
        self.setCentralWidget(widget)

        self.eat_timer = QtCore.QTimer()
        QtCore.QObject.connect(self.eat_timer, QtCore.SIGNAL("timeout()"), self.eat)
        self.eat_timer.start(100)

    def eat(self):
        self.model.eat()
        self.update()

if __name__ == '__main__':
    import feeders, sys
    from model import TimeSeries

    if len(sys.argv) >= 2 and sys.argv[1] == '--modeeg':
        feed = feeders.mk_modeeg(sys.stdin) # read modeeg data from stdin
    else:
        feed = feeders.random_positive_sinoids

    app = QtGui.QApplication(['Dantien'])
    window = Dantien(TimeSeries(feed))
    window.show()
    app.exec_()
