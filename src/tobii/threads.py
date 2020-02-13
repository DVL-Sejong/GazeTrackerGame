import re

from PyQt5.QtCore import QThread, QTimer, QTime, QEventLoop


class CardThread(QThread):

    def in_process(self):
        self.time = self.time.addMSecs(30)
        index = self.time.msecsSinceStartOfDay()

        if index < 20: return

        if self.is_finished: self.terminate()

        if len(self.list) == 0:
            for i in range(index):
                self.list.append(self.parser.is_in_range(self.screen_size,
                                                         self.x, self.y,
                                                         self.i, self.j,
                                                         self.proportion))
        else:
            self.list.pop(0)
            self.list.append(self.parser.is_in_range(self.screen_size,
                                                         self.x, self.y,
                                                         self.i, self.j,
                                                         self.proportion))

        red, green, blue = self.get_rgb()
        if self.list.count(True) / len(self.list) >= 0.6:
            red, green, blue = self.rgb_to_black(red, green, blue)
            self.set_rgb(red, green, blue)
            if self.is_black():
                self.terminate()
        else:
            red, green, blue = self.rgb_to_white(red, green, blue)
            if self.is_initial_color() is False:
                self.set_rgb(red, green, blue)

    def __init__(self, label, parser, screen_size, i, j, proportion):
        QThread.__init__(self)
        self.timer = QTimer()
        self.timer.moveToThread(self)
        self.timer.timeout.connect(self.in_process)
        self.time = QTime(0, 0, 0)
        self.label = label
        self.parser = parser
        self.screen_size = screen_size
        self.x = 0
        self.y = 0
        self.i = i
        self.j = j
        self.proportion = proportion
        self.list = []
        self.is_finished = False

    def run(self):
        self.timer.start(30)
        loop = QEventLoop()
        loop.exec_()

    def get_rgb(self):
        stylesheet = self.label.styleSheet()
        regex = r"[Rr][Gg][Bb][\(](((([\d]{1,3})[\,]{0,1})[\s]*){3})[\)]"
        rgb = re.search(regex, stylesheet).groups()
        return int(rgb[1]), int(rgb[2]), int(rgb[3])

    def rgb_to_black(self, red, green, blue):
        return red - 1, green - 1, blue - 1

    def rgb_to_white(self, red, green, blue):
        return red + 1, green + 1, blue + 1

    def set_rgb(self, red, green, blue):
        if red < 0 or green < 0 or blue < 0: return
        if red > 255 or green > 255 or blue > 255: return
        stylesheet = "background-color: rgb(%d, %d, %d);" % (red, green, blue)
        self.label.setStyleSheet(stylesheet)

    def is_black(self):
        red, green, blue = self.get_rgb()
        return True if red == 0 and green == 0 and blue == 0 else False

    def is_initial_color(self):
        red, green, blue = self.get_rgb()
        return True if red == 160 and green == 160 and blue == 160 else False