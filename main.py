import os
from random import choice
from math import floor
import pygame

from tile import Tile, TILE_TYPE
from camera import Camera
from popup import Popup

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

        # pygame.display.set_icon(icon_image)
        # background.blit(background_image, (0, 0))
        self.camera = Camera(100, 100)

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
        all = pygame.sprite.RenderUpdates()

        # set up containers for collision detection etc
        Tile.images = [
            resources["images"]["grass"],
            resources["images"]["water"],
            resources["images"]["sand"]
        ]
        Tile.containers = all, self.tiles

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
        selected_tile = None
        popup = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_f:
                        pygame.display.toggle_fullscreen()

            keys = pygame.key.get_pressed()
            camera_dx = (keys[pygame.K_LEFT] - keys[pygame.K_RIGHT]) * CAMERA_SPEED
            camera_dy = (keys[pygame.K_UP] - keys[pygame.K_DOWN]) * CAMERA_SPEED

            relative_cursor_position = self.camera.apply_to_point(pygame.mouse.get_pos())
            mouse_grid_ref = Tile.convert_point_to_grid_ref(relative_cursor_position)

            if pygame.mouse.get_pressed()[0]:
                selected_tile = None

            for tile in self.tiles:
                tile.is_hovered = tile.check_hover(mouse_grid_ref)
                if pygame.mouse.get_pressed()[0] and tile.is_hovered:
                    selected_tile = tile

            self.all.clear(self.screen, self.background)
            self.all.update()
            self.camera.update((camera_dx, camera_dy))

            for sprite in self.all:
                self.screen.blit(sprite.image, self.camera.apply(sprite))

            if selected_tile:
                popup = Popup(self.screen, 'dummy', 'content')


            pygame.display.flip()

            self.clock.tick(40)

if __name__ == "__main__":
    game = Game()
    game.game_loop()
