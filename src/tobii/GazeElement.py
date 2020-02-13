import math

from src.tobii.objects import Point, Pupil, Size, Type


class GazeElement:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.id = 0
        self.screen_size = Size(0, 0)
        self.status = 0
        self.timestamp = 0
        self.left_point = Point(0, 0, 0)
        self.right_point = Point(0, 0, 0)
        self.average_point = Point(0, 0, 0)
        self.left_pupil = Pupil(0, 0)
        self.right_pupil = Pupil(0, 0)
        self.average_pupil = Pupil(0, 0)

    def initialize(self, screen_size):
        self.id = self.raw_data.get('id')
        self.screen_size.set(screen_size)
        self.status = self.raw_data.get('status')
        self.timestamp = self.raw_data.get('device_time_stamp')
        self.extract_points()
        self.calibrate(screen_size)
        self.extract_pupils()

    def extract_points(self):
        self.left_point = self.extract_point(Type.LEFT)
        self.right_point = self.extract_point(Type.RIGHT)
        self.average_point = self.calculate_average_point()

    def extract_point(self, direction):
        validity_attribute = '_gaze_point_validity'
        coordinate_attribute = '_gaze_point_on_display_area'
        attribute = 'left' if direction is Type.LEFT else 'right'

        validity = self.raw_data.get(attribute + validity_attribute)
        x = self.raw_data.get(attribute + coordinate_attribute)[0]
        y = self.raw_data.get(attribute + coordinate_attribute)[1]

        if math.isnan(x) or math.isnan(y):
            validity = 0
            x = 0 if math.isnan(y) else x
            y = 0 if math.isnan(y) else y

        return Point(x, y, validity)

    def calculate_average_point(self):
        validity = 0
        x = 0
        y = 0
        if self.left_point.validity == 1 and self.right_point.validity == 1:
            x = (self.left_point.x + self.right_point.x) / 2
            y = (self.left_point.y + self.right_point.y) / 2
            validity = 1

        return Point(x, y, validity)

    def calibrate(self, screen_size):
        self.left_point.x *= screen_size.width
        self.left_point.y *= screen_size.height
        self.right_point.x *= screen_size.width
        self.right_point.y *= screen_size.height

    def extract_pupils(self):
        self.left_pupil.diameter = self.raw_data.get('left_pupil_diameter')
        if math.isnan(self.left_pupil.diameter): self.left_pupil.diameter = 0
        self.left_pupil.validity = self.raw_data.get('left_pupil_validity')
        self.right_pupil.diameter = self.raw_data.get('right_pupil_diameter')
        if math.isnan(self.right_pupil.diameter): self.right_pupil.diameter = 0
        self.right_pupil.validity = self.raw_data.get('right_pupil_validity')
        self.average_pupil = self.calculate_average_pupil()

    def calculate_average_pupil(self):
        diameter = 0
        validity = 0
        if self.left_pupil.validity == 1 and self.right_pupil.validity == 1:
            diameter = (self.left_pupil.diameter + self.right_pupil.diameter) / 2
            validity = 1
        return Pupil(diameter, validity)
