from operator import eq

from src.exception import Error


def is_number(string):
    try:
        value = int(string)
    except ValueError:
        try:
            value = float(string)
        except ValueError:
            return False
    return True


def is_value_number(value, title):
    error = Error()
    if is_number(value):
        if float(value) == 0:
            error.set_message(title + "CANNOT be 0!")
        return error
    else:
        error.set_message("Input of " + title + " is Not Number!")
        return error


class Inputs:
    def __init__(self,
                 lineEdit_pupiltimer,
                 lineEdit_seqsize,
                 lineEdit_boardsizen,
                 lineEdit_boardsizem,
                 sequence,
                 lineEdit_dwell):
        self.lineEdit_pupiltimer = lineEdit_pupiltimer
        self.lineEdit_seqsize = lineEdit_seqsize
        self.lineEdit_boardsizen = lineEdit_boardsizen
        self.lineEdit_boardsizem = lineEdit_boardsizem
        self.sequence = sequence
        self.lineEdit_dwell = lineEdit_dwell
        self.seqsize = 0

    def is_all_filled_properly(self):
        pupil_timer = self.is_pupil_timer_number()
        if pupil_timer.is_true: return pupil_timer
        seqsize = self.is_seqsize_number()
        if seqsize.is_true: return seqsize
        is_seq_filled = self.is_seq_filled()
        if is_seq_filled.is_true: return is_seq_filled
        boardsize = self.is_board_filled()
        if boardsize.is_true: return boardsize
        is_board_filled = self.is_board_filled()
        if is_board_filled.is_true: return is_board_filled
        dwell_timer = self.is_dwell_timer_numer()
        if dwell_timer.is_true: return dwell_timer

    def is_pupil_timer_number(self):
        error = is_value_number(self.lineEdit_pupiltimer.displayText(), "Pupil Timer")
        return error

    def is_seqsize_number(self):
        error = is_value_number(self.lineEdit_seqsize.displayText(), "Sequence Size")
        if int(self.lineEdit_seqsize.displayText()) > 8: error.set_message("8 is Maximum Number!")
        return error

    def is_boardsize_number(self):
        error = is_value_number(self.lineEdit_boardsizem.displayText(), "Row")
        if int(self.lineEdit_boardsizem.displayText()) > 5: error.set_message("5 is Maximum Number!")
        error = is_value_number(self.lineEdit_boardsizen.displayText(), "Column")
        if int(self.lineEdit_boardsizen.displayText()) > 5: error.set_message("5 is Maximum Number!")
        return error

    def is_seq_filled(self):
        error = Error()
        if self.seqsize == 0:
            error.set_message("Enter Sequence Size!")
            return error
        for i in range(self.seqsize):
            if eq(self.sequence.elements[i], ""):
                error.set_message("%dth Sequence is Not Filled!" % (i + 1))
                return error
        return error

    def is_board_filled(self):
        error = Error()
        for i in range(self.lineEdit_boardsizen):
            for j in range(self.lineEdit_boardsizem):
                if eq(self.sequence.matrix[i][j], ""):
                    error.set_message("(%d, %d) Board Value is Not Filled!" % (i + 1, j + 1))
                    return error
        return error

    def is_dwell_timer_numer(self):
        error = is_value_number(self.lineEdit_dwell.displayText(), "Dwell Timer")
        return error
