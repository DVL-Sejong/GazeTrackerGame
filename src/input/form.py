import random
import string
import time
from datetime import datetime
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
                 lineEdit_dbid,
                 checkBox_dbid,
                 lineEdit_pupiltimer,
                 lineEdit_seqsize,
                 lineEdit_seqtimer,
                 lineEdit_boardsizen,
                 lineEdit_boardsizem,
                 sequence,
                 card,
                 lineEdit_dwell):
        self.lineEdit_dbid = lineEdit_dbid
        self.checkBox_dbid = checkBox_dbid
        self.lineEdit_pupiltimer = lineEdit_pupiltimer
        self.lineEdit_seqsize = lineEdit_seqsize
        self.lineEdit_seqtimer = lineEdit_seqtimer
        self.lineEdit_boardsizen = lineEdit_boardsizen
        self.lineEdit_boardsizem = lineEdit_boardsizem
        self.sequence = sequence
        self.card = card
        self.lineEdit_dwell = lineEdit_dwell
        self.seqsize = 0

    def is_all_filled_properly(self):
        pupil_timer = self.is_pupil_timer_number()
        if pupil_timer.is_true: return pupil_timer
        seqsize = self.is_seqsize_number()
        if seqsize.is_true: return seqsize
        seqtimer = self.is_seqtimer_number()
        if seqtimer.is_true: return seqtimer
        is_seq_filled = self.is_seq_filled()
        if is_seq_filled.is_true: return is_seq_filled
        boardsize = self.is_boardsize_number()
        if boardsize.is_true: return boardsize
        board_filled = self.is_board_filled()
        if board_filled.is_true: return board_filled
        card = self.is_card_filled()
        if card.is_true: return card
        dwell_timer = self.is_dwell_timer_numer()
        if dwell_timer.is_true: return dwell_timer
        return Error()

    def is_pupil_timer_number(self):
        error = is_value_number(self.lineEdit_pupiltimer.displayText(), "Pupil Timer")
        return error

    def is_seqsize_number(self):
        error = is_value_number(self.lineEdit_seqsize.displayText(), "Sequence Size")
        if int(self.lineEdit_seqsize.displayText()) > 8: error.set_message("8 is Maximum Number!")
        return error

    def is_seqtimer_number(self):
        error = is_value_number(self.lineEdit_seqtimer.displayText(), "Sequence Timer")
        return error

    def is_boardsize_number(self):
        error = is_value_number(self.lineEdit_boardsizem.displayText(), "Row")
        if len(self.lineEdit_boardsizem.displayText()) == 0: error.set_message("m is NOT Entered!")
        if error.is_true: return error
        if int(self.lineEdit_boardsizem.displayText()) > 5: error.set_message("5 is Maximum Number!")
        if error.is_true: return error
        error = is_value_number(self.lineEdit_boardsizen.displayText(), "Column")
        if len(self.lineEdit_boardsizen.displayText()) == 0: error.set_message("n is NOT Entered!")
        if error.is_true: return error
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
        for i in range(int(self.lineEdit_boardsizem.displayText())):
            for j in range(int(self.lineEdit_boardsizen.displayText())):
                if eq(self.sequence.matrix[i][j].displayText(), ""):
                    error.set_message("(%d, %d) Board Value is Not Filled!" % (i + 1, j + 1))
                    return error
        return error

    def is_card_filled(self):
        width = is_value_number(self.card.width.displayText(), "Card Width")
        if width.is_true: return width
        height = is_value_number(self.card.height.displayText(), "Card Height")
        if height.is_true: return height
        horizontal_margin = is_value_number(self.card.horizontal_margin.displayText(), "Horizontal Margin")
        if horizontal_margin.is_true: return horizontal_margin
        vertical_margin = is_value_number(self.card.vertical_margin.displayText(), "Vertical Margin")
        if vertical_margin.is_true: return vertical_margin
        return Error()

    def is_dwell_timer_numer(self):
        error = is_value_number(self.lineEdit_dwell.displayText(), "Dwell Timer")
        return error


class Basic:
    def __init__(self):
        self.lineEdit_pupiltimer = 10
        self.lineEdit_seqsize = 4
        self.lineEdit_seqtimer = 5
        self.lineEdit_boardsizen = 3
        self.lineEdit_boardsizem = 4
        self.lineEdit_width = 300
        self.lineEdit_height = 300
        self.lineEdit_marginh = 80
        self.lineEdit_marginv = 80
        self.lineEdit_dwell = 3000

    def generate_sequence(self, seqsize, n, m):
        sequence = []
        upper_alphabet = string.ascii_uppercase
        maximum = n * m
        while True:
            random.seed(time.time())
            random_letter = random.choice(upper_alphabet)
            if random_letter not in sequence and ord(random_letter) < 65 + maximum:
                sequence.append(random_letter)
            if len(sequence) == seqsize: return sequence

    def generate_matrix(self, n, m):
        matrix = []
        sequence = self.generate_sequence(n * m, n, m)

        index = 0
        for i in range(m):
            row = []
            for j in range(n):
                row.append(sequence[index])
                index += 1
            matrix.append(row)

        return matrix
