import pygame
from enum import Enum
import src.groups as groups

class DECORATIONS(Enum):
  TREE = 0

class Decoration(pygame.sprite.Sprite):
  images = []

  def __init__(self, decoration_type, position, offset_x, offset_y):
    print(position)
    offset_position = list(position)
    offset_position[0] = offset_position[0] + offset_x
    offset_position[1] = offset_position[1] + offset_y
    pygame.sprite.Sprite.__init__(self, (groups.all, groups.decorations, groups.layeredItems))
    self.type = decoration_type
    self.default_image = self.images[self.type.value]
    self.hover_image = self.images[self.type.value].copy()
    self.hover_image.fill((10,10,10), rect=None, special_flags=pygame.BLEND_RGB_ADD)
    self.image = self.default_image
    self.rect = self.image.get_rect(topleft=tuple(offset_position))
    self.default_position = position