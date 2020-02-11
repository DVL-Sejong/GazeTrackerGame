import sys
from operator import eq

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from gui.main import Ui_MainWindow
from src.database import Database
from src.exception import Error


def warn(error):
    if error.is_true is False: return

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(error.message)
    msg.setWindowTitle("Error")
    msg.show()
    msg.exec_()


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_objects()
        self.add_button_clicked()
        self.add_checkbox_changed()
        self.add_edit_entered()
        self.hide_boxes()

    def init_objects(self):
        self.database = Database(self.table, self.lineEdit_dbid, self.checkBox_dbid)
        self.error = Error()

    def add_button_clicked(self):
        self.pushButton_shortcuts.clicked.connect(self.on_click)
        self.pushButton_dbsetting.clicked.connect(self.on_click)
        self.pushButton_start.clicked.connect(self.on_click)
        self.pushButton_ok.clicked.connect(self.on_shortcuts_click)
        self.pushButton_cancel.clicked.connect(self.on_database_click)
        self.pushButton_apply.clicked.connect(self.on_database_click)

    def add_checkbox_changed(self):
        self.checkBox_dbid.stateChanged.connect(self.on_change)

    def add_edit_entered(self):
        self.lineEdit_dbid.returnPressed.connect(self.on_enter)

    def hide_boxes(self):
        self.box_detailed.hide()
        self.box_board.hide()

    @pyqtSlot()
    def on_click(self):
        sending_button = self.sender()
        if eq(sending_button.objectName(), "pushButton_shortcuts"):
            self.stack.setCurrentWidget(self.page_shortcuts)
        if eq(sending_button.objectName(), "pushButton_dbsetting"):
            self.stack.setCurrentWidget(self.page_database)
        if eq(sending_button.objectName(), "pushButton_start"):
            print("checking")

    @pyqtSlot()
    def on_shortcuts_click(self):
        sending_button = self.sender()
        if eq(sending_button.objectName(), "pushButton_ok"):
            self.stack.setCurrentWidget(self.page_main)

    @pyqtSlot()
    def on_database_click(self):
        sending_button = self.sender()
        if eq(sending_button.objectName(), "pushButton_cancel"):
            self.database.on_cancel_click()
            self.stack.setCurrentWidget(self.page_main)
        if eq(sending_button.objectName(), "pushButton_apply"):
            warn(self.database.on_apply_click())
            self.stack.setCurrentWidget(self.page_main)

    def on_change(self):
        if self.checkBox_dbid.isChecked():
            warn(self.database.on_id_apply())

    def on_enter(self):
        sending_edit = self.sender()
        if eq(sending_edit.objectName(), "lineEdit_dbid"):
            warn(self.database.on_id_apply())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
