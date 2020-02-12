from operator import eq

from src.game.status import Status
from src.input.parser import Parser


class Designer:
    def __init__(self, inputs, card):
        self.inputs = inputs
        self.card = card
        self.parser = Parser(inputs)
        self.count = 0

    def set_sequence_card(self):
        size = self.inputs.seqsize
        sequence = self.inputs.sequence.elements
        width, height = self.parser.get_card_size()
        horizontal_margin, vertical_margin = self.parser.get_margins()

        for i in range(size):
            self.card.sequence[i].setText(sequence[i])
            self.card.sequence[i].setFixedWidth(width)
            self.card.sequence[i].setFixedHeight(height)

        self.card.seq_layout.setContentsMargins(horizontal_margin / 2, 0, horizontal_margin / 2, 0)

    def set_game_card(self):
        n, m = self.parser.get_matrix_size()
        matrix = self.inputs.sequence.matrix
        width, height = self.parser.get_card_size()
        horizontal_margin, vertical_margin = self.parser.get_margins()
        horizontal_margin = horizontal_margin / 2
        vertical_margin = vertical_margin / 2

        for i in range(n):
            for j in range(m):
                self.card.game[i][j].setText(matrix[i][j].displayText())
                self.card.game[i][j].setFixedWidht(width)
                self.card.game[i][j].setFixedHeight(height)

        self.card.game_layout.setContentsMargins(horizontal_margin, vertical_margin, horizontal_margin, vertical_margin)

    def remove_number(self, i, j):
        if eq(self.card.geme[i][j].displayText(), ""): return

        for element in self.inputs.sequence.elements:
            if eq(self.card.geme[i][j].displayText(), element):
                self.card.game[i][j].setText("")
                self.count += 1
                return

    def is_all_fixated(self):
        return True if self.count == self.inputs.seqsize else False
