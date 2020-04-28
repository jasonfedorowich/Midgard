from vector2d import Vector2D


class Camera:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.vector = Vector2D()
        self.updated = False

    def update_viewport(self, x, y):
        self.vector.x += x
        self.vector.y += y
        self.updated = True

    def increment_x(self, val):
        self.vector.x += val
        self.updated = True

