import math

from src.game.status import Status


class Parser:

    def __init__(self, inputs):
        self.inputs = inputs

    def pupil_time(self):
        return float(self.inputs.lineEdit_pupiltimer.displayText()) * 1000

    def sequence_time(self):
        return float(self.inputs.lineEdit_seqtimer.displayText()) * 1000

    def seqsize(self):
        return int(self.inputs.lineEdit_seqsize.displayText())

    def dwell_time(self):
        return float(self.inputs.lineEdit_dwell.displayText())

    def width(self):
        return float(self.inputs.card.width.displayText())

    def height(self):
        return float(self.inputs.card.height.displayText())

    def horizontal_margin(self):
        return float(self.inputs.card.horizontal_margin.displayText())

    def vertical_margin(self):
        return float(self.inputs.card.vertical_margin.displayText())

    def matrix_width(self):
        return float(self.inputs.lineEdit_boardsizen.displayText())

    def matrix_height(self):
        return float(self.inputs.lineEdit_boardsizem.displayText())

    def get_matrix_size(self):
        n = int(self.inputs.lineEdit_boardsizen.displayText())
        m = int(self.inputs.lineEdit_boardsizem.displayText())
        return n, m

    def get_time(self, status):
        if status == Status.PUPIL:
            return self.pupil_time()
        elif status == Status.SEQUENCE:
            return self.sequence_time()
        elif status == Status.GAME:
            return 2000 * 1000

    def get_dwell_rgb(self):
        dwell = self.dwell_time()
        return int((dwell / 30) - 20)

    def get_card_size(self):
        width = self.width()
        height = self.height()
        return width, height

    def get_margins(self):
        horizontal_margin = self.horizontal_margin()
        vertical_margin = self.vertical_margin()
        return horizontal_margin, vertical_margin

    def get_total_size(self):
        card_width, card_height = self.get_card_size()
        n, m = self.get_matrix_size()
        horizontal_space, vertical_space = self.get_margins()
        total_width = (n * card_width) + ((n - 1) * horizontal_space)
        total_height = (m * card_height) + ((m - 1) * vertical_space)
        return total_width, total_height

    def get_distance(self, i, j):
        card_width, card_height = self.get_card_size()
        horizontal_space, vertical_space = self.get_margins()
        width_distance = (j * card_width) + (j * horizontal_space)
        height_distance = (i * card_height) + (i * vertical_space)
        return width_distance, height_distance

    def get_starting_point(self, screen_size, i, j):
        screen_width = screen_size.width
        screen_height = screen_size.height
        total_width, total_height = self.get_total_size()
        distance_width, distance_height = self.get_distance(i, j)
        x = ((screen_width - total_width) / 2) + distance_width
        y = ((screen_height - total_height) / 2) + distance_height
        return x, y

    def get_center_point(self, screen_size, i, j):
        card_width, card_height = self.get_card_size()
        starting_x, starting_y = self.get_starting_point(screen_size, i, j)
        x = starting_x + (card_width / 2)
        y = starting_y + (card_height / 2)
        return x, y

    def get_proportional_size(self, proportion):
        card_width, card_height = self.get_card_size()
        width = card_width * proportion
        height = card_height * proportion
        return width, height

    def is_in_range(self, screen_size, x, y, i, j, proportion):
        center_x, center_y = self.get_center_point(screen_size, i, j)
        proportional_width, proportional_height = self.get_proportional_size(proportion)
        distance = math.sqrt(pow(x - center_x, 2) + pow(y - center_y, 2))
        if distance <= min(proportional_width, proportional_height):
            return True
        else:
            return False

