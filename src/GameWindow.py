import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from gui.game import Ui_GameWindow


class GameWindow(QMainWindow, Ui_GameWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameWindow()
    ex.show()
    sys.exit(app.exec_())
