import math
import random
from prisonereconomy.config import max_movement


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
        math.atan(slope(*self.coordinates))

    def r(self):
        return distance(Point([0, 0]), self)

    def move(self, point, toward):
        move_distance = random.uniform(-max_movement, max_movement)
        angle = math.atan(slope(self, point))
        vector = point_from_polar(angle, move_distance)
        if not toward:
            vector = point_from_polar(angle + math.pi, move_distance)
        new_coordinates = (self.x() + vector.x(), self.y() + vector.y())
        if distance(self, Point(*new_coordinates)) > distance(self, point):
            new_coordinates = (point.x(), point.y())
        self.coordinates = new_coordinates


def slope(a, b):
    if b[0] - a[0] != 0:
        return b[1] - a[1] / b[0] - a[0]
    else:
        return math.inf


def distance(a, b):
    return math.sqrt(((a.x - b.x) ** 2) + (a.y - b.y ** 2))


def point_from_polar(theta, r):
    return Point([r * math.cos(theta), r * math.sin(theta)])
