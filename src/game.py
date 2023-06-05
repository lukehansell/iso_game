'''Entry point for running a game

This class holds most of the logic regarding how a game runs.
It controls the game loop, event handling, state management
and rendering.
'''

import os
import pygame

import src.groups as groups
import src.style as style

from data.level import level

from .sprites.tile import Tile, TileType
from .sprites.decoration import Decoration, DECORATIONS
from .sprites.popup import Popup
from .sprites.build_menu import BuildMenu
from .sprites.game_info_box import GameInfoBox

from .state.build_mode import BUILD_MODES

from .state.default_state import state as default_state
from .state import reducer as state_reducer

from .state.events import (
    create_display_popup,
    create_hide_popup,
    create_toggle_build_mode,
    create_game_tick
)

from .lib.projection import grid_ref_to_iso, iso_to_grid_ref

CAMERA_SPEED = 5
HEIGHT = 600
WIDTH = 800

SCREENRECT = pygame.Rect(0, 0, WIDTH, HEIGHT)

def _init_screen():
    winstyle = 0
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    pygame.display.set_caption('isometric test')

    return screen

def _init_background(screen):
    background = pygame.Surface(screen.get_size()).convert()
    screen.blit(background, (0, 0))
    pygame.display.flip()

    return background

def _init_game_resources(screen_size, on_tile_click):
    resources = _load_resources()

    # set up containers for collision detection etc
    Tile.images = [
        resources["images"]["grass"],
        resources["images"]["water"],
        resources["images"]["sand"],
        resources["images"]['residential'],
        resources["images"]["tree"]
    ]

    Decoration.images = [
        resources["images"]["tree"]
    ]

    for y, row in enumerate(level['tiles']):
        for x, tile in enumerate(row):
            if tile is not None:
                Tile(
                    TileType(tile),
                    grid_ref_to_iso((x, y), x_offset=-32, y_offset=-79),
                    (x, y),
                    on_tile_click
                )

    build_menu = BuildMenu(50+style.padding*2, width=screen_size.width, on_build_option_select=_on_build_option_select)
    GameInfoBox((screen_size.width/2, build_menu.rect.bottom), layer=1)

def _load_resources():
    return {
        "images": {
            "grass": load_image('grass.png').convert_alpha(),
            "water": load_image('water.png').convert_alpha(),
            "sand": load_image('sand.png').convert_alpha(),
            "residential": load_image('residential.png').convert_alpha(),
            "tree": load_image('tree.png').convert_alpha()
        }
    }

def _on_popup_close():
    create_hide_popup()

def _on_build_option_select(mode):
    create_toggle_build_mode(mode)

def load_image(image):
    '''Loads given filename and returns pygame image'''
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../assets/images', image)
    return pygame.image.load(path)

class Game():
    '''
        Game object

        Methods
        -------
        game_loop():
            Maintains the continuous loop of the game.
            Updates game objects and renders to the screen


    '''
    def __init__(self):
        '''
            Initialises the game, creating the screen, background, resources and state
        '''
        pygame.init()
        pygame.font.init()
        self.__clock = pygame.time.Clock()
        self.__state = state_reducer(default_state, None)

        self.__screen = _init_screen()
        self.__background = _init_background(self.__screen)
        _init_game_resources(self.__screen.get_rect(), self.__tile_click)

        self.__popup = None
        # pygame.display.set_icon(icon_image)

    def game_loop(self):
        '''
            Creates a loop while the game is not in a quitting state.
            Creates a game ticks on loop (with configurable delay)
            Handles clicking on the screen
            Updates all items
            Calls draw to update the screen
        '''
        tick = 0
        camera = self.__state.get('camera')
        camera.camera.left = SCREENRECT.width/2
        camera.camera.centery = SCREENRECT.height/2 - (64 * len(level))

        while not self.__state['system']['is_quitting']:
            prev_state = self.__state.copy()
            for event in pygame.event.get():
                self.__state = state_reducer(self.__state, event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__handle_click(event)

            tick += 1
            # 40 fps * (3 - speed setting) e.g 40 * (3 - 0) = 3 second tick
            if tick >= 40 * (3 - self.__state.get('game').get('speed')):
                create_game_tick(groups.tiles.sprites())
                tick = 0

            self.__state.get('camera').update()
            groups.all.update(self.__state)
            groups.overlays.update(self.__state)

            # popup display updates
            if prev_state['ui']['popup'] != self.__state['ui']['popup']:
                if self.__state['ui']['popup'] is not None:
                    self.__popup = Popup(
                        title=self.__state['ui']['popup']['title'],
                        on_close=_on_popup_close
                    )

                elif self.__popup is not None:
                    self.__popup = self.__popup.kill()

            self.__draw(self.__state, prev_state)

    def __draw(self, state, prev_state):
        if state['system']['is_fullscreen'] != prev_state['system']['is_fullscreen']:
            pygame.display.toggle_fullscreen()

        groups.all.clear(self.__screen, self.__background)

        self.__background.fill(style.black)
        self.__screen.blit(self.__background, (0, 0))

        for sprite in groups.camera_relative:
            self.__screen.blit(sprite.image, self.__state.get('camera').apply(sprite))
            for decoration_row in sprite.decorations:
                for decoration in decoration_row:
                    if decoration is not None:
                        self.__screen.blit(decoration.image, self.__state.get('camera').apply(decoration))

        groups.overlays.draw(self.__screen)

        pygame.display.flip()

        self.__clock.tick(40)

    def __handle_click(self, event):
        mouse_position = event.pos
        sprites = groups.layeredItems.get_sprites_at(mouse_position)

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
        camera_relative_mouse_position = self.__state['camera'].apply_to_point(mouse_position)
        tile_grid_ref = iso_to_grid_ref(camera_relative_mouse_position)
        sprite = next((tile for tile in groups.tiles.sprites() if tile.is_at_grid_reference(tile_grid_ref)), None)
        if sprite is not None:
            on_click = getattr(sprite, 'on_click', None)

            if callable(on_click):
                on_click()

    def __tile_click(self, tile):
        if self.__state['build_mode'] is not None:
            if self.__state['build_mode'] == BUILD_MODES.RESIDENTIAL:
                tile.set_tile_type(TileType.RESIDENTIAL)
                tile.clear_decorations()

        else:
            titles = {
                TileType.GRASS: 'Grass',
                TileType.SAND: 'Sand',
                TileType.WATER: 'Water',
                TileType.RESIDENTIAL: 'Residential'
            }
            title = f'{titles.get(tile.type)}'

            create_display_popup(title, 'bar')
