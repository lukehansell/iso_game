from enum import Enum
import pygame

class TILE_TYPE(Enum):
    GRASS = 0
    WATER = 1
    SAND = 2

class Tile(pygame.sprite.Sprite):
    images = []

    def __init__(self, type, position, map_position):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.type = type
        self.default_image = self.images[self.type.value]
        self.hover_image = self.images[self.type.value].copy()
        self.hover_image.fill((10,10,10), rect=None, special_flags=pygame.BLEND_RGB_ADD)
        self.image = self.default_image
        self.rect = self.image.get_rect(topleft=position)
        self.position = position
        self.is_hovered = False
        self.map_position = map_position

    def update(self):
        if self.is_hovered:
            self.image = self.hover_image
        else:
            self.image = self.default_image

    def check_hover(self, point):
        return point == self.map_position

    @classmethod
    def create_position(cls, x, y, x_offset, y_offset):
        return (x_offset + (x * 31) - (y * 31), y_offset + x * 18 + y * 18)

    @classmethod
    def convert_point_to_grid_ref(cls, point):
        (x, y) = point

        grid_x = ((18*x)+(31*y))/1116
        grid_y = (y - (18*grid_x))/18
        return (round(grid_x)-1, round(grid_y))