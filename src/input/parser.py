from src.game.status import Status


class Parser:

    def __init__(self, inputs):
        self.inputs = inputs

    def pupil_time(self):
        return self.inputs.lineEdit_pupiltimer.displayText() * 1000

    def sequence_time(self):
        return self.inputs.lineEdit_seqtimer.displayText() * 1000

    def dwell_time(self):
        return self.inputs.lineEdit_dwell.displayText()

    def width(self):
        return self.inputs.card.width.displayText()

    def height(self):
        return self.inputs.card.height.displayText()

    def horizontal_margin(self):
        return self.inputs.card.horizontal_margin.displayText()

    def vertical_margin(self):
        return self.inputs.card.vertical_margin.displayText()

    def get_time(self, status):
        if status == Status.PUPIL:
            return self.pupil_time()
        elif status == Status.SEQUENCE:
            return self.sequence_time()
        elif status == Status.GAME:
            return self.dwell_time()

    def get_card_size(self):
        width = self.width()
        height = self.height()
        return width, height

    def get_margins(self):
        horizontal_margin = self.horizontal_margin()
        vertical_margin = self.vertical_margin()
        return horizontal_margin, vertical_margin

    def get_matrix_size(self):
        n = self.inputs.lineEdit_boardsizen.displayText()
        m = self.inputs.lineEdit_boardsizem.displayText()
        return n, m