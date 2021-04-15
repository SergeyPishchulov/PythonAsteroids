import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, count):
        return Vector(self.x * count, self.y * count)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __rmul__(self, count):
        return self * count

    def __sub__(self, other):
        negative = other * (-1)
        return self + negative

    def normalize(self, length):
        k = self.length() / length
        self.x /= k
        self.y /= k
