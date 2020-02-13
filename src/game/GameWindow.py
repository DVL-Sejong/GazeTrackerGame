import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication

from gui.game import Ui_GameWindow
from src.game.designer import Designer
from src.game.status import Status
from src.game.timer import GameTimer, SplashTimer
from src.input.parser import Parser
from src.tobii.tracker import Tobii


class GameWindow(QMainWindow, Ui_GameWindow):

    def __init__(self, MainWindow, inputs):
        super().__init__()
        self.setupUi(self)
        self.main = MainWindow
        self.inputs = inputs
        self.init_objects()

        self.tobii = Tobii(self)
        self.start(Status.PUPIL, self.page_pupil)
        self.tobii.run()

    def init_ui(self):
        self.stackedWidget.setCurrentWidget(self.page_pupil)

    def init_objects(self):
        self.parser = Parser(self.inputs)
        self.designer = Designer(self.inputs, self.parser, self.card)

    def on_time(self):
        self.timer = GameTimer()
        self.timer.finished.connect(self.on_finish)
        self.timer.duration = self.parser.get_time(self.status)
        self.timer.start()

    def on_finish(self):
        if self.status == Status.PUPIL:
            self.splash(Status.SPLASH_SEQUENCE)
        elif self.status == Status.SPLASH_SEQUENCE:
            self.start(Status.SEQUENCE, self.page_sequence)
        elif self.status == Status.SEQUENCE:
            self.splash(Status.SPLASH_GAME)
        elif self.status == Status.SPLASH_GAME:
            self.start(Status.GAME, self.page_game)
        elif self.status == Status.GAME:
            self.splash(Status.SPLASH_END)
        elif self.status == Status.SPLASH_END:
            data = self.tobii.end()
            self.deleteLater()
            self.main.on_game_finish(data)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_Space:
            self.tobii.is_wandering = True

    def start(self, status, page):
        self.change_status(status)
        self.change_page(page)
        self.init_screen()
        self.on_time()

    def splash(self, status):
        self.change_status(status)
        self.change_page(self.page_splash)
        self.splash_timer = SplashTimer(status, self.label_count)
        self.splash_timer.finished.connect(self.on_finish)
        self.splash_timer.start()

    def change_status(self, status):
        self.status = status

    def change_page(self, page):
        self.stackedWidget.setCurrentWidget(page)

    def init_screen(self):
        if self.status == Status.SEQUENCE:
            self.designer.set_sequence_card()
        elif self.status == Status.GAME:
            self.designer.set_game_card()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = GameWindow()
#     ex.show()
#     sys.exit(app.exec_())
