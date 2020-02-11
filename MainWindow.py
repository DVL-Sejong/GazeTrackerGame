import sys
from operator import eq

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication

from gui.main import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_button_clicked()

    def add_button_clicked(self):
        self.pushButton_shortcuts.clicked.connect(self.on_click)
        self.pushButton_ok.clicked.connect(self.on_shortcuts_click)

    @pyqtSlot()
    def on_click(self):
        sending_button = self.sender()
        if eq(sending_button.objectName(), "pushButton_shortcuts"):
            self.stack.setCurrentWidget(self.page_shortcuts)

    @pyqtSlot()
    def on_shortcuts_click(self):
        sending_button = self.sender()
        if eq(sending_button.objectName(), "pushButton_ok"):
            self.stack.setCurrentWidget(self.page_main)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())