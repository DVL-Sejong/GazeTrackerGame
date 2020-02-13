import re

import pyautogui as pyautogui
import tobii_research as tr
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer, QTime, QEventLoop
from PyQt5.QtCore import QThread, pyqtSignal

from src.game.status import Status
from src.input.parser import Parser
from src.tobii.RawData import RawData
from src.tobii.organizer import Organizer
from src.tobii.objects import Size


class Tobii():
    def __init__(self, GameWindow, inputs):
        self.window = GameWindow
        self.window_size = Size(pyautogui.size().width, pyautogui.size().height)
        self.inputs = inputs
        self.parser = Parser(inputs)
        self.tobii = tr.find_all_eyetrackers()[0]
        self.data = []
        self.plot_thread = PlotThread(self.window)
        self.plot_thread.signal.connect(self.on_plot)
        self.is_wandering = False

    def run(self):
        self.tobii.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.plot_thread.gaze_data_callback, as_dictionary=True)

    def end(self):
        # self.window.card_thread.terminate()
        self.tobii.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.plot_thread.gaze_data_callback)
        self.plot_thread.terminate()
        organize_data = Organizer(self.data)
        return organize_data

    def on_plot(self, element):
        element.is_wandering = self.is_wandering
        self.data.append(element)
        self.is_wandering = False
        if self.window.status == Status.GAME:
            self.set_point(element)

        # if self.data[-1].is_validate(constant.AVERAGE):
        #     self.paint.left = self.data.data[-1].left_point
        #     self.paint.right = self.data.data[-1].right_point
        #     self.paint.average = self.data.data[-1].average_point
        #     self.paint.repaint()

    def set_point(self, element):
        if element.average_point.validity == 0:
            x = 0
            y = 0
        else:
            x = element.average_point.x
            y = element.average_point.y

        # self.window.card_thread.x = x
        # self.window.card_thread.y = y
        for thread in self.window.card_threads:
            thread.x = x
            thread.y = y


class PlotThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, GameWindow):
        QThread.__init__(self)
        self.window = GameWindow
        self.window_size = Size(pyautogui.size().width, pyautogui.size().height)

    def run(self):
        print("running")

    def gaze_data_callback(self, gaze_data):
        raw = RawData(self.window_size, self.window.status)
        element = raw.gaze_data_callback(gaze_data)
        self.signal.emit(element)
