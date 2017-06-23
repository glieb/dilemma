import math
import random
from config import max_movement


class Point:

    def __init__(self, coordinates):
        self.coordinates = coordinates

    def __getitem__(self, index):
        return self.coordinates[index]

    def x(self):
        return self.coordinates[0]

    def y(self):
        return self.coordinates[1]

    def theta(self):
        math.atan2(slope(Point((0, 0)), self))

    def r(self):
        return distance(Point((0, 0)), self)

    def move(self, point, toward):
        move_distance = random.uniform(0, max_movement)
        if move_distance > (distance(self, point) / 2.0) and toward:  # if trying to move past the midpoint
            move_distance = distance(self, point) / 2.0               # move to the midpoint instead
        angle = math.atan2(point.y() - self.y(), point.x() - self.x())
        if not toward:
            angle += math.pi  # reverse angle
        vector = point_from_polar(angle, move_distance)
        new_coordinates = (self.x() + vector.x(), self.y() + vector.y())
        self.coordinates = new_coordinates


def slope(a, b):  # as of now, this function may be obsolete.
    if b[0] - a[0] != 0:
        return (b[1] - a[1]) / (b[0] - a[0])
    else:
        return math.inf


def distance(a, b):
    return math.sqrt(((a.x() - b.x()) ** 2) + ((a.y() - b.y()) ** 2))


def point_from_polar(theta, r):
    return Point((r * math.cos(theta), r * math.sin(theta)))
