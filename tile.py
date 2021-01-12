from enum import Enum
import pygame
import groups
from state.build_mode import BUILD_MODES
from state.events import create_purchase

class TILE_TYPE(Enum):
    GRASS = 0
    WATER = 1
    SAND = 2
    RESIDENTIAL = 3

def create_tile_opts(is_populated=False, environment_impact=0, happiness_impact=0, cost=0):
    return {
        'is_populated' : is_populated,
        'environment_impact' : environment_impact,
        'happiness_impact': happiness_impact,
        'cost': cost
    }

game_logic = {
    TILE_TYPE.GRASS: create_tile_opts(environment_impact=10, happiness_impact=1),
    TILE_TYPE.WATER: create_tile_opts(environment_impact=10, happiness_impact=1),
    TILE_TYPE.SAND: create_tile_opts(environment_impact=1, happiness_impact=1),
    TILE_TYPE.RESIDENTIAL: create_tile_opts(is_populated=True, cost=50000)
}

class TileStats():
    def __init__(self):
        self.population = 0
        self.environmental_rating = 0
        self.happiness_rating = 0
class Tile(pygame.sprite.Sprite):
    images = []

    def __init__(self, type, position, map_position, on_click=None):
        pygame.sprite.Sprite.__init__(self, (groups.all, groups.tiles, groups.camera_relative, groups.layeredItems))
        self.type = type
        self.default_image = self.images[self.type.value]
        self.hover_image = self.images[self.type.value].copy()
        self.hover_image.fill((10,10,10), rect=None, special_flags=pygame.BLEND_RGB_ADD)
        self.image = self.default_image
        self.rect = self.image.get_rect(topleft=position)
        self.position = position
        self.map_position = map_position
        self.click_handler = on_click

        self.stats = TileStats()

    def on_click(self):
        if callable(self.click_handler):
            self.click_handler(self)

    def update(self, state):
        if self.check_hover(state.get('camera').apply_to_point(state['system']['mouse_position'])):
            if state['build_mode'] is not None:
                if state['build_mode'] == BUILD_MODES.RESIDENTIAL:
                    self.image = self.images[TILE_TYPE.RESIDENTIAL.value].copy()
                self.image.set_alpha(200)

                if self.type == TILE_TYPE.WATER or self.type == TILE_TYPE.RESIDENTIAL:
                    self.image.fill((255, 0, 0), rect=None, special_flags=pygame.BLEND_RGB_MULT)
            else:
                self.image = self.images[self.type.value].copy()
                self.image.fill((10,10,10), rect=None, special_flags=pygame.BLEND_RGB_ADD)
        else:
            self.image = self.images[self.type.value]

    def check_hover(self, point):
        return Tile.convert_point_to_grid_ref(point) == self.map_position

    def is_at_grid_reference(self, grid_reference):
        return grid_reference == self.map_position

    def set_tile_type(self, type):
        if self.type is not TILE_TYPE.WATER and self.type is not TILE_TYPE.RESIDENTIAL:
            self.type = type
            create_purchase(game_logic[type]['cost'])


    def game_tick(self):
        settings = game_logic[self.type]
        if settings['is_populated']:
            self.stats.population += 10 # TODO make this smarter

    @classmethod
    def create_position(cls, x, y, x_offset, y_offset):
        return (x_offset + (x * 31) - (y * 31), y_offset + x * 18 + y * 18 - 64)

    @classmethod
    def convert_point_to_grid_ref(cls, point):
        (x, y) = point

        grid_x = ((18*x)+(31*y))/1116
        grid_y = (y - (18*grid_x))/18
        return (round(grid_x)-1, round(grid_y))