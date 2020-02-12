from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QEventLoop, QTime


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