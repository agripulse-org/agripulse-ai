from enum import Enum


class SoilType(str, Enum):
    SANDY = "sandy"
    LOAMY = "loamy"
    BLACK = "black"
    RED = "red"
    CLAYEY = "clayey"
