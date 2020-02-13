from enum import Enum


class Status(Enum):
    PUPIL = 0
    SPLASH_SEQUENCE = 3
    SEQUENCE = 1
    SPLASH_GAME = 4
    GAME = 2
    SPLASH_END = 5
