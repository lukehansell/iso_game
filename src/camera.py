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
        '''offsets the entity by the cameras position

            Args:
                entity (Object with rect attribute of type Rect): the object the camera position is to be applied to

            Returns:
                Returns a Rect of the entities position offset by the camera position
        '''
        return entity.rect.move(self.camera.topleft)

    def apply_to_point(self, point):
        '''offsets a point by the cameras position

            Args:
                point (tuple: (:int,:int)): Tuple of (x,y) to be moved

            Returns:
                Tuple of (int, int) for the x, y of the offset point
        '''
        (camera_x, camera_y) = self.camera.topleft
        (point_x, point_y) = point
        return (point_x/self.zoom - camera_x/self.zoom, point_y/self.zoom - camera_y/self.zoom)

    def update(self):
        '''moves the camera by the dx and dy values in its state'''
        (x, y) = self.camera.topleft
        self.camera = pg.Rect(x + self.dx, y + self.dy, self.width, self.height)
