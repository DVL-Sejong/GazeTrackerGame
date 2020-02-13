import re
from operator import eq

from PyQt5.QtCore import QThread, QTimer, QTime, QEventLoop


class Designer:
    def __init__(self, inputs, parser, card):
        self.inputs = inputs
        self.parser = parser
        self.card = card
        self.count = 0

    def set_sequence_card(self):
        size = self.inputs.seqsize
        sequence = self.inputs.sequence.elements
        width, height = self.parser.get_card_size()
        horizontal_margin, vertical_margin = self.parser.get_margins()

        for i in range(8):
            self.card.sequence[i].hide()

        for i in range(size):
            self.card.sequence[i].setText(sequence[i].displayText())
            self.card.sequence[i].setFixedWidth(width)
            self.card.sequence[i].setFixedHeight(height)
            self.card.sequence[i].show()

        self.card.seq_layout.setSpacing(horizontal_margin)

    def set_game_card(self):
        n, m = self.parser.get_matrix_size()
        matrix = self.inputs.sequence.matrix
        width, height = self.parser.get_card_size()
        horizontal_margin, vertical_margin = self.parser.get_margins()

        for i in range(5):
            for j in range(5):
                self.card.game[i][j].hide()

        for i in range(m):
            for j in range(n):
                self.card.game[i][j].setText(matrix[i][j].displayText())
                self.card.game[i][j].setFixedWidth(width)
                self.card.game[i][j].setFixedHeight(height)
                self.card.game[i][j].show()

        self.card.game_layout.setHorizontalSpacing(horizontal_margin)
        self.card.game_layout.setVerticalSpacing(vertical_margin)

    def remove_number(self, i, j):
        if eq(self.card.geme[i][j].displayText(), ""): return

        for element in self.inputs.sequence.elements:
            if eq(self.card.geme[i][j].displayText(), element):
                self.card.game[i][j].setText("")
                self.count += 1
                return

    def is_all_fixated(self):
        return True if self.count == self.inputs.seqsize else False
