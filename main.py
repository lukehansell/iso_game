import os
from random import choice
from math import floor
import pygame

from tile import Tile, TILE_TYPE
from camera import Camera
from popup import Popup

from state.default_state import state as default_state
from state import reducer as state_reducer

from state.events import create_select_tile_event, create_deselect_tile_event, create_display_popup, create_hide_popup

import groups

CAMERA_SPEED = 5
HEIGHT = 600
WIDTH = 800

SCREENRECT = pygame.Rect(0, 0, WIDTH, HEIGHT)

def load_image(image):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', image)
    return pygame.image.load(path)

class Game():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.screen = self.init_screen()
        self.background = self.init_background(self.screen)
        self.resources = self.load_resources()
        self.all = self.init_game_resources(self.resources)

        self.state = state_reducer(default_state, None)
        self.popup = None
        # pygame.display.set_icon(icon_image)

    def init_screen(self):
        winstyle = 0
        bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
        screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

        pygame.display.set_caption('isometric test')

        return screen

    def init_background(self, screen):
        background = pygame.Surface(screen.get_size()).convert()
        background.fill((0,0,0))
        screen.blit(background, (0, 0))
        pygame.display.flip()

        return background

    def init_game_resources(self, resources):
        self.tiles = groups.tiles
        self.overlays = groups.overlays
        self.layeredItems = groups.layeredItems
        self.camera_relative = groups.camera_relative

        all = groups.all

        # set up containers for collision detection etc
        Tile.images = [
            resources["images"]["grass"],
            resources["images"]["water"],
            resources["images"]["sand"]
        ]

        for y in range(100):
            for x in range(100):
                tile = choice([0, 1, 2])
                Tile(TILE_TYPE(tile), Tile.create_position(x, y, 0, 0), (x, y), self.tile_click)

        return all

    def load_resources(self):
        return {
            "images": {
                "grass": load_image('grass.png').convert_alpha(),
                "water": load_image('water.png').convert_alpha(),
                "sand": load_image('sand.png').convert_alpha()
            }
        }

    def game_loop(self):
        while not self.state['system']['is_quitting']:
            prev_state = self.state.copy()
            for event in pygame.event.get():
                self.state = state_reducer(self.state, event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event)

            self.state.get('camera').update()
            self.all.update(self.state)
            self.overlays.update(self.state)

            # popup display updates
            if prev_state['ui']['popup'] != self.state['ui']['popup']:
                if self.state['ui']['popup'] is not None:
                    self.popup = Popup(self.state['ui']['popup']['content'], self.state['ui']['popup']['title'], on_close=self.on_popup_close)
                elif self.popup is not None:
                    self.popup = self.popup.kill()

            self.draw(self.state, prev_state)

    def handle_click(self, event):
        mouse_position = event.pos
        sprites = self.layeredItems.get_sprites_at(mouse_position)

        if sprites is not None and len(sprites) > 0:
            if isinstance(sprites[-1], Tile):
                # if it's a tile we need to figure out the correct projected tile clicked
                tile_grid_ref = Tile.convert_point_to_grid_ref(mouse_position)
                sprite = next((tile for tile in self.tiles.sprites() if tile.is_at_grid_reference(tile_grid_ref)), None)
            else:
                sprite = sprites[-1]

            if sprite is not None:
                on_click = getattr(sprite, 'on_click', None)

                if callable(on_click):
                    on_click()

    def draw(self, state, prev_state):
        if state['system']['is_fullscreen'] != prev_state['system']['is_fullscreen']:
            pygame.display.toggle_fullscreen()

        self.all.clear(self.screen, self.background)

        self.background.fill((0,0,0))
        self.screen.blit(self.background, (0, 0))

        for sprite in self.camera_relative:
            self.screen.blit(sprite.image, self.state.get('camera').apply(sprite))

        self.overlays.draw(self.screen)

        pygame.display.flip()

        self.clock.tick(40)

    def tile_click(self, tile):
        titles = {
            TILE_TYPE.GRASS: 'Grass',
            TILE_TYPE.SAND: 'Sand',
            TILE_TYPE.WATER: 'Water'
        }
        title = f'Tile Type: {titles.get(tile.type)}'

        create_display_popup(title, 'bar')

    def on_popup_close(self):
        create_hide_popup()

if __name__ == "__main__":
    game = Game()
    game.game_loop()
