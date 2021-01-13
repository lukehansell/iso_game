import pygame as pg
class Camera:
    def __init__(self, width, height, position = (0, 0)):
        self.camera = pg.Rect(position[0], position[1], width, height)
        self.width = width
        self.height = height
        self.dx = 0
        self.dy = 0
        self.zoom = 1

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_to_point(self, point):
        (camera_x, camera_y) = self.camera.topleft
        (point_x, point_y) = point
        return (point_x/self.zoom - camera_x/self.zoom, point_y/self.zoom - camera_y/self.zoom)

    def update(self):
        (x, y) = self.camera.topleft
        self.camera = pg.Rect(x + self.dx, y + self.dy, self.width, self.height)
