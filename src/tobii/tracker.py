import tobii_research as tr
from PyQt5.QtCore import QThread, pyqtSignal

from src.tobii.RawData import RawData
from src.tobii.organizer import Organizer
from src.tobii.objects import Size


class Tobii():
    def __init__(self, GameWindow):
        self.window = GameWindow
        self.window_size = Size(GameWindow.size().width(), GameWindow.size().height())
        self.tobii = tr.find_all_eyetrackers()[0]
        self.data = []
        self.plot_thread = PlotThread(self.window)
        self.plot_thread.signal.connect(self.on_plot)

    def run(self):
        self.tobii.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.plot_thread.gaze_data_callback, as_dictionary=True)

    def end(self):
        self.tobii.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.plot_thread.gaze_data_callback)
        self.plot_thread.terminate()

        organize_data = Organizer(self.data)
        return organize_data

    def on_plot(self, element):
        self.data.append(element)

        # if self.data[-1].is_validate(constant.AVERAGE):
        #     self.paint.left = self.data.data[-1].left_point
        #     self.paint.right = self.data.data[-1].right_point
        #     self.paint.average = self.data.data[-1].average_point
        #     self.paint.repaint()


class PlotThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, GameWindow):
        QThread.__init__(self)
        self.window = GameWindow
        self.window_size = Size(GameWindow.size().width(), GameWindow.size().height())

    def run(self):
        print("running")

    def gaze_data_callback(self, gaze_data):
        raw = RawData(self.window_size, self.window.status)
        element = raw.gaze_data_callback(gaze_data)
        self.signal.emit(element)



