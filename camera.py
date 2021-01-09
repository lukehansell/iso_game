import pygame as pg
class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_to_point(self, point):
        (camera_x, camera_y) = self.camera.topleft
        (point_x, point_y) = point
        return (point_x - camera_x, point_y - camera_y)

    def update(self, target):
        (dx, dy) = target
        (x, y) = self.camera.topleft
        self.camera = pg.Rect(x + dx, y + dy, self.width, self.height)