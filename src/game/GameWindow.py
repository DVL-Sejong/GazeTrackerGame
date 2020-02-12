import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from gui.game import Ui_GameWindow
from src.game.designer import Designer
from src.game.status import Status
from src.game.timer import GameTimer
from src.input.parser import Parser


class GameWindow(QMainWindow, Ui_GameWindow):

    def __init__(self, inputs):
        super().__init__()
        self.setupUi(self)
        self.inputs = inputs
        self.init_objects()

        self.start(Status.PUPIL, self.page_pupil)

    def init_objects(self):
        self.parser = Parser(self.inputs)
        self.designer = Designer(self.inputs, self.card)

    def on_finish(self):
        if self.status == Status.PUPIL:
            self.start(Status.SEQUENCE, self.page_sequence)
        elif self.status == Status.SEQUENCE:
            self.start(Status.GAME, self.page_game)
        elif self.status == Status.GAME:
            print("game")

    def start(self, status, page):
        self.change_page(status, page)
        self.init_screen()
        self.timer = GameTimer()
        self.timer.finished.connect(self.on_finish)
        self.timer.duration = self.parser.get_time(self.status)
        self.timer.start()

    def change_page(self, status, page):
        self.status = status
        self.stackedWidget.setCurrentWidget(page)

    def init_screen(self):
        if self.status == Status.PUPIL:
            print("pupil")
        elif self.status == Status.SEQUENCE:
            self.designer.set_sequence_card()
        elif self.status == Status.GAME:
            self.designer.set_game_card()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = GameWindow()
#     ex.show()
#     sys.exit(app.exec_())
