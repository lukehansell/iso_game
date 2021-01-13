import os
import pygame

from .sprites.tile import Tile, TILE_TYPE
from .sprites.popup import Popup
from .sprites.build_menu import BuildMenu

from .state.build_mode import BUILD_MODES

from .state.default_state import state as default_state
from .state import reducer as state_reducer

from .state.events import (
    create_display_popup,
    create_hide_popup,
    create_toggle_build_mode,
    create_game_tick
)

from .lib import grid_ref_to_iso, iso_to_grid_ref

import src.groups as groups

from data.level import level

CAMERA_SPEED = 5
HEIGHT = 600
WIDTH = 800

SCREENRECT = pygame.Rect(0, 0, WIDTH, HEIGHT)

def load_image(image):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../assets/images', image)
    return pygame.image.load(path)

class Game():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.state = state_reducer(default_state, None)

        self.screen = self.init_screen()
        self.background = self.init_background(self.screen)
        self.resources = self.load_resources()
        self.all = self.init_game_resources(self.resources)

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
        screen.blit(background, (0, 0))
        pygame.display.flip()

        return background

    def init_game_resources(self, resources):
        self.tiles = groups.tiles
        self.overlays = groups.overlays
        self.layeredItems = groups.layeredItems
        self.camera_relative = groups.camera_relative

        everything = groups.all

        # set up containers for collision detection etc
        Tile.images = [
            resources["images"]["grass"],
            resources["images"]["water"],
            resources["images"]["sand"],
            resources["images"]['residential']
        ]

        for y, row in enumerate(level['tiles']):
            for x, tile in enumerate(row):
                if tile is not None:
                    Tile(TILE_TYPE(tile), grid_ref_to_iso((x, y),x_offset=-32, y_offset=-79), (x, y), self.tile_click)

        BuildMenu(self.screen.get_rect().height, on_build_option_select=self.on_build_option_select)

        return everything

    def load_resources(self):
        return {
            "images": {
                "grass": load_image('grass.png').convert_alpha(),
                "water": load_image('water.png').convert_alpha(),
                "sand": load_image('sand.png').convert_alpha(),
                "residential": load_image('residential.png').convert_alpha()
            }
        }

    def game_loop(self):
        tick = 0
        camera = self.state.get('camera')
        camera.camera.left = SCREENRECT.width/2
        camera.camera.centery = SCREENRECT.height/2 - (64 * len(level))
        while not self.state['system']['is_quitting']:
            prev_state = self.state.copy()
            for event in pygame.event.get():
                self.state = state_reducer(self.state, event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event)

            tick += 1
            # 40 fps * (3 - speed setting) e.g 40 * (3 - 0) = 3 second tick
            if tick >= 40 * (3 - self.state.get('game').get('speed')):
                create_game_tick(self.tiles.sprites())
                tick = 0

            self.state.get('camera').update()
            self.all.update(self.state)
            self.overlays.update(self.state)

            # popup display updates
            if prev_state['ui']['popup'] != self.state['ui']['popup']:
                if self.state['ui']['popup'] is not None:
                    self.popup = Popup(title=self.state['ui']['popup']['title'], on_close=self.on_popup_close)
                elif self.popup is not None:
                    self.popup = self.popup.kill()

            self.draw(self.state, prev_state)

    def handle_click(self, event):
        mouse_position = event.pos
        sprites = self.layeredItems.get_sprites_at(mouse_position)

        # check for click of anything but tiles
        if sprites is not None and len(sprites) > 0:
            if not isinstance(sprites[-1], Tile):
                sprite = sprites[-1]

                if sprite is not None:
                    on_click = getattr(sprite, 'on_click', None)

                    if callable(on_click):
                        on_click()
                        return

        # if we've not clicked on anything yet then assume we want the game world not overlays
        camera_relative_mouse_position = self.state['camera'].apply_to_point(mouse_position)
        tile_grid_ref = iso_to_grid_ref(camera_relative_mouse_position)
        sprite = next((tile for tile in self.tiles.sprites() if tile.is_at_grid_reference(tile_grid_ref)), None)
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
        if self.state['build_mode'] is not None:
            if self.state['build_mode'] == BUILD_MODES.RESIDENTIAL:
                tile.set_tile_type(TILE_TYPE.RESIDENTIAL)

        else:
            titles = {
                TILE_TYPE.GRASS: 'Grass',
                TILE_TYPE.SAND: 'Sand',
                TILE_TYPE.WATER: 'Water',
                TILE_TYPE.RESIDENTIAL: 'Residential'
            }
            title = f'{titles.get(tile.type)}'

            create_display_popup(title, 'bar')

    def on_popup_close(self):
        create_hide_popup()

    def on_build_option_select(self, mode):
        create_toggle_build_mode(mode)