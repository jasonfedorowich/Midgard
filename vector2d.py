from cmath import sqrt


class Vector2D:

    def __init__(self):
        self.x = 0.0
        self.y = 0.0

    def distance(self, vector):
        return sqrt((self.x - vector.x) ** 2 + (self.y - vector.y) ** 2)
