import os
from random import choice
from math import floor
import pygame

from tile import Tile, TILE_TYPE
from camera import Camera
from popup import Popup

from state.default_state import state as default_state
from state import reducer as state_reducer

from state.events import create_select_tile_event, create_deselect_tile_event

map = [
    [0,0,0,0,0],
    [0,1,1,0,0],
    [0,1,1,0,0],
    [0,1,0,0,None],
    [0,0,0,None,None]
]

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
        self.popup = Popup(self.screen, 'dummy', 'content', onClose=self.onPopupClose)

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
        self.tiles = pygame.sprite.Group()
        self.overlays = pygame.sprite.Group()
        all = pygame.sprite.RenderUpdates()

        # set up containers for collision detection etc
        Tile.images = [
            resources["images"]["grass"],
            resources["images"]["water"],
            resources["images"]["sand"]
        ]
        Tile.containers = all, self.tiles

        Popup.containers = self.overlays

        for y in range(100):
            for x in range(100):
                tile = choice([0, 1, 2])
                Tile(TILE_TYPE(tile), Tile.create_position(x, y, 0, 0), (x, y))

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
            self.state = state_reducer(self.state, pygame.event.poll())

            if pygame.mouse.get_pressed()[0] and self.state.get('selected_tile'):
                create_deselect_tile_event()

            self.all.update(self.state)
            self.overlays.update(self.state)

            self.draw(self.state, prev_state)

    def draw(self, state, prev_state):
        if state['system']['is_fullscreen'] != prev_state['system']['is_fullscreen']:
            pygame.display.toggle_fullscreen()

        self.all.clear(self.screen, self.background)
        self.overlays.clear(self.screen, self.background)

        self.background.fill((0,0,0))
        self.screen.blit(self.background, (0, 0))

        for sprite in self.all:
            self.screen.blit(sprite.image, self.state.get('camera').apply(sprite))

        self.overlays.draw(self.screen)

        pygame.display.flip()

        self.clock.tick(40)

    def onPopupClose(self):
        if self.popup:
            self.popup.kill()

if __name__ == "__main__":
    game = Game()
    game.game_loop()
