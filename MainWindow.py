import sys
from operator import eq

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from gui.main import Ui_MainWindow
from src.GameWindow import GameWindow
from src.database import Database
from src.exception import Error
from src.form import Inputs


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
        self.form = Inputs(self.lineEdit_dbid, self.checkBox_dbid,
                           self.lineEdit_pupiltimer, self.lineEdit_seqsize,
                           self.lineEdit_boardsizen, self.lineEdit_boardsizem, self.sequence,
                           self.card, self.lineEdit_dwell,
                           self.radioButton_on, self.radioButton_off)
        self.error = Error()

    def add_button_clicked(self):
        self.pushButton_shortcuts.clicked.connect(self.on_click)
        self.pushButton_dbsetting.clicked.connect(self.on_click)
        self.pushButton_seqsize.clicked.connect(self.on_click)
        self.pushButton_boardsize.clicked.connect(self.on_click)
        self.pushButton_start.clicked.connect(self.on_click)
        self.pushButton_ok.clicked.connect(self.on_shortcuts_click)
        self.pushButton_cancel.clicked.connect(self.on_database_click)
        self.pushButton_apply.clicked.connect(self.on_database_click)

    def add_checkbox_changed(self):
        self.checkBox_dbid.stateChanged.connect(self.on_change)

    def add_edit_entered(self):
        self.lineEdit_dbid.returnPressed.connect(self.on_enter)
        self.lineEdit_pupiltimer.returnPressed.connect(self.on_enter)
        self.lineEdit_seqsize.returnPressed.connect(self.on_enter)
        self.lineEdit_boardsizem.returnPressed.connect(self.on_enter)

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
        if eq(sending_button.objectName(), "pushButton_seqsize"):
            self.show_sequence_matrix()
        if eq(sending_button.objectName(), "pushButton_boardsize"):
            self.show_board_matrix()
        if eq(sending_button.objectName(), "pushButton_start"):
            self.game()

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
        if eq(sending_edit.objectName(), "lineEdit_pupiltimer"):
            warn(self.form.is_pupil_timer_number())
        if eq(sending_edit.objectName(), "lineEdit_seqsize"):
            self.show_sequence_matrix()
        if eq(sending_edit.objectName(), "lineEdit_boardsizem"):
            self.show_board_matrix()

    def show_sequence_matrix(self):
        error = self.form.is_seqsize_number()
        warn(error)
        if error.is_true is False:
            self.form.seqsize = int(self.lineEdit_seqsize.displayText())
            self.box_detailed.show()
            for element in self.form.sequence.elements:
                element.hide()
            for i in range(self.form.seqsize):
                self.form.sequence.elements[i].show()

    def show_board_matrix(self):
        error = self.form.is_boardsize_number()
        warn(error)
        if error.is_true is False:
            self.box_board.show()
            for i in range(5):
                for j in range(5):
                    self.form.sequence.matrix[i][j].hide()
            for i in range(int(self.lineEdit_boardsizem.displayText())):
                for j in range(int(self.lineEdit_boardsizen.displayText())):
                    self.form.sequence.matrix[i][j].show()

    def game(self):
        error = self.form.is_all_filled_properly()
        warn(error)
        if error.is_true is False:
            self.game_window = GameWindow(self.form)
            self.game_window.showFullScreen()
            self.game_window.setFixedSize(self.game_window.size())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
