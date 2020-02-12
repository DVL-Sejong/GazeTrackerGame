import sys

from PyQt5.QtCore import QThread, QTimer, QEventLoop, QTime
from PyQt5.QtWidgets import QMainWindow, QApplication

from gui.game import Ui_GameWindow


class GameTimer(QThread):

    def in_process(self):
        self.time = self.time.addMSecs(1)
        if self.time.msecsSinceStartOfDay() >= self.duration: self.terminate()

    def __init__(self, *args, **kwargs):
        QThread.__init__(self)
        self.timer = QTimer()
        self.timer.moveToThread(self)
        self.timer.timeout.connect(self.in_process)
        self.time = QTime(0, 0, 0)
        self.duration = 0

    def reset_timer(self, duration):
        self.duration = duration
        self.time.setHMS(0, 0, 0)

    def run(self):
        self.timer.start(1)
        loop = QEventLoop()
        loop.exec_()


class GameWindow(QMainWindow, Ui_GameWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.timer = GameTimer()
        self.timer.reset_timer(3000)
        self.timer.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameWindow()
    ex.show()
    sys.exit(app.exec_())
