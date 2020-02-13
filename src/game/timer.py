from PyQt5.QtCore import QThread, QTimer, QEventLoop, QTime

from src.game.status import Status


class GameTimer(QThread):
    def in_process(self):
        self.time = self.time.addMSecs(1)
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


class SplashTimer(QThread):
    def in_process(self):
        self.time = self.time.addSecs(1)
        if self.status == Status.SPLASH_END and self.time.msecsSinceStartOfDay() >= 3000:
            self.terminate()
        if self.status != Status.SPLASH_END:
            if self.count > 0:
                self.label.setText(str(self.count))
            elif self.count == 0:
                self.label.setText("")
            elif self.count == -1:
                self.terminate()
            self.count -= 1

    def __init__(self, status, label):
        QThread.__init__(self)
        self.timer = QTimer()
        self.timer.moveToThread(self)
        self.timer.timeout.connect(self.in_process)
        self.time = QTime(0, 0, 0)
        self.status = status
        self.label = label
        self.count = 5
        self.init_label()

    def run(self):
        self.timer.start(1000)
        loop = QEventLoop()
        loop.exec_()

    def init_label(self):
        if self.status == Status.SPLASH_END:
            self.label.setText("")
        else:
            self.label.setText(str(self.count))
            self.count -= 1
