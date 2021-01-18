from enum import Enum
import pygame
import src.groups as groups
from src.state.build_mode import BUILD_MODES
from src.state.events import create_purchase
from src.lib.projection import iso_to_grid_ref

class TileType(Enum):
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
    TileType.GRASS: create_tile_opts(environment_impact=10, happiness_impact=1),
    TileType.WATER: create_tile_opts(environment_impact=10, happiness_impact=1),
    TileType.SAND: create_tile_opts(environment_impact=1, happiness_impact=1),
    TileType.RESIDENTIAL: create_tile_opts(is_populated=True, cost=50000)
}

class TileStats():
    def __init__(self):
        self.population = 0
        self.environmental_rating = 0
        self.happiness_rating = 0

class Tile(pygame.sprite.Sprite):
    images = []

    def __init__(self, tile_type, position, grid_ref, on_click=None):
        pygame.sprite.Sprite.__init__(self, (groups.all, groups.tiles, groups.camera_relative, groups.layeredItems))
        self.type = tile_type
        self.default_image = self.images[self.type.value]
        self.hover_image = self.images[self.type.value].copy()
        self.hover_image.fill((10,10,10), rect=None, special_flags=pygame.BLEND_RGB_ADD)
        self.image = self.default_image
        self.rect = self.image.get_rect(topleft=position)
        self.default_position = position
        self.grid_ref = grid_ref
        self.click_handler = on_click

        self.decorations = [[None] * 8] * 8

        self.stats = TileStats()

    def on_click(self):
        if callable(self.click_handler):
            self.click_handler(self)

    def update(self, state):
        if self.check_hover(state.get('camera').apply_to_point(state['system']['mouse_position'])):
            if state['build_mode'] is not None:
                if state['build_mode'] == BUILD_MODES.RESIDENTIAL:
                    self.image = self.images[TileType.RESIDENTIAL.value].copy()
                self.image.set_alpha(200)

                if self.type == TileType.WATER or self.type == TileType.RESIDENTIAL:
                    self.image.fill((255, 0, 0), rect=None, special_flags=pygame.BLEND_RGB_MULT)
            else:
                self.image = self.images[self.type.value].copy()
                self.image.fill((10,10,10), rect=None, special_flags=pygame.BLEND_RGB_ADD)
        else:
            self.image = self.images[self.type.value]

        # correct image scale to zoom
        zoom = state.get('camera').zoom
        default_width = 64
        default_height = 132
        ( default_x, default_y ) = self.default_position
        self.image = pygame.transform.scale(self.image, (default_width * zoom, default_height * zoom))
        self.rect = self.image.get_rect(topleft=(default_x * zoom, default_y * zoom ))

    def check_hover(self, point):
        return iso_to_grid_ref(point) == self.grid_ref

    def is_at_grid_reference(self, grid_reference):
        return grid_reference == self.grid_ref

    def set_tile_type(self, new_type):
        if self.type is not TileType.WATER and self.type is not TileType.RESIDENTIAL:
            self.type = new_type
            create_purchase(game_logic[new_type]['cost'])

    def game_tick(self):
        settings = game_logic[self.type]
        if settings['is_populated']:
            self.stats.population += 10 # TODO make this smarter
