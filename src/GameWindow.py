import sys
from enum import Enum

from PyQt5.QtCore import QThread, QTimer, QEventLoop, QTime, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication

from gui.game import Ui_GameWindow


class Status(Enum):
    PUPIL = 1
    SEQUENCE = 2
    GAME = 3


class GameTimer(QThread):
    signal = pyqtSignal()

    def in_process(self):
        self.time = self.time.addMSecs(1)
        print(self.time.msecsSinceStartOfDay())
        if self.time.msecsSinceStartOfDay() >= self.duration:
            self.terminate()

    def __init__(self, *args, **kwargs):
        QThread.__init__(self)
        self.timer = QTimer()
        self.timer.moveToThread(self)
        self.timer.timeout.connect(self.in_process)
        self.time = QTime(0, 0, 0)
        self.duration = 0

    def run(self):
        self.timer.start(1)
        loop = QEventLoop()
        loop.exec_()


class GameWindow(QMainWindow, Ui_GameWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.status = Status.PUPIL
        self.start(3000)

    def on_finish(self):
        if self.status == Status.PUPIL:
            self.change_status(Status.SEQUENCE, self.page_sequence)
            self.start(5000)
        elif self.status == Status.SEQUENCE:
            self.change_status(Status.GAME, self.page_game)
            self.start(1000000)
        elif self.status == Status.GAME:
            print("game")

    def change_status(self, status, page):
        self.status = status
        self.stackedWidget.setCurrentWidget(page)

    def start(self, duration):
        self.timer = GameTimer()
        self.timer.finished.connect(self.on_finish)
        self.timer.duration = duration
        self.timer.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameWindow()
    ex.show()
    sys.exit(app.exec_())
