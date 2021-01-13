import pygame as py
from sprites.text import Text
from groups import overlays, layeredItems, all

class GameInfoBox(py.sprite.Sprite):
    def __init__(self, position, layer=1, size=(500, 150)):
        py.sprite.Sprite.__init__(self, (all, overlays, layeredItems))

        self._layer = layer

        surface = py.Surface(size)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)

        py.draw.rect(surface, (255,255,255), py.Rect(0, 0, size[0], size[1]), border_radius=10)

        self.cash_balance_text = Text(f'', (position[0], 15), is_centered=True, font_size=32, color=(0,0,0), layer=self._layer+1)

    def update(self, state):
        self.cash_balance_text.kill()
        self.cash_balance_text = Text(f'${state["game"]["balance"]}', (250, 15), is_centered=True, font_size=32, color=(0,0,0), layer=self._layer+1)