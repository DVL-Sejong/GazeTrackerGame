from datetime import datetime

from src.tobii.GazeElement import GazeElement


class RawData:
    def __init__(self, screen_size, status):
        self.screen_size = screen_size
        self.status = status
        self.left_gaze_point_on_display_area = []
        self.right_gaze_point_on_display_area = []
        self.left_gaze_point_validity = []
        self.right_gaze_point_validity = []
        self.left_pupil_diameter = []
        self.left_pupil_validity = []
        self.right_pupil_diameter = []
        self.right_pupil_validity = []
        self.device_time_stamp = []

    def gaze_data_callback(self, gaze_data):
        self.left_gaze_point_on_display_area.append(gaze_data['left_gaze_point_on_display_area'])
        self.right_gaze_point_on_display_area.append(gaze_data['right_gaze_point_on_display_area'])
        self.left_gaze_point_validity.append(gaze_data['left_gaze_point_validity'])
        self.right_gaze_point_validity.append(gaze_data['right_gaze_point_validity'])
        self.left_pupil_diameter.append(gaze_data['left_pupil_diameter'])
        self.left_pupil_validity.append(gaze_data['left_pupil_validity'])
        self.right_pupil_diameter.append(gaze_data['right_pupil_diameter'])
        self.right_pupil_validity.append(gaze_data['right_pupil_validity'])
        self.device_time_stamp.append(gaze_data['device_time_stamp'])
        element = self.to_element()
        return element

    def to_element(self):
        index = len(self.left_gaze_point_on_display_area) - 1

        dictionary = {
            'left_gaze_point_on_display_area': self.left_gaze_point_on_display_area[index],
            'right_gaze_point_on_display_area': self.right_gaze_point_on_display_area[index],
            'left_gaze_point_validity': self.left_gaze_point_validity[index],
            'right_gaze_point_validity': self.right_gaze_point_validity[index],
            'left_pupil_diameter': self.left_pupil_diameter[index],
            'left_pupil_validity': self.left_pupil_validity[index],
            'right_pupil_diameter': self.right_pupil_diameter[index],
            'right_pupil_validity': self.right_pupil_validity[index],
            'device_time_stamp': self.device_time_stamp[index],
            'status': self.status
        }

        element = GazeElement(dictionary)
        element.initialize(self.screen_size)
        return element
