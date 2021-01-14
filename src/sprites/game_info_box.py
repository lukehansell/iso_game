import pygame as py
from src.groups import overlays, layeredItems, all as all_sprites
import src.style as style
from .text import Text

class GameInfoBox(py.sprite.Sprite):
    def __init__(self, position, layer=1, size=(350, 75)):
        py.sprite.Sprite.__init__(self, (all_sprites, overlays, layeredItems))

        self._layer = layer

        surface = py.Surface(size)

        self.image = surface
        self.rect = self.image.get_rect(midtop=position)

        py.draw.rect(
            surface,
            style.white,
            py.Rect(0, 0, size[0], size[1]),
            border_bottom_left_radius=style.border_radius,
            border_bottom_right_radius=style.border_radius
        )

        self.cash_balance_text = self.render_cash_balance_text('-')
        self.population_text = self.render_population_text('-')

    def update(self, state):
        self.cash_balance_text.kill()
        self.cash_balance_text = self.render_cash_balance_text(state["game"]["balance"])

    def render_cash_balance_text(self, balance):
        return Text(f'cash balance: ${balance}', (self.rect.centerx, 20), is_centered=True, font_size=32, color=style.black)

    def render_population_text(self, population):
        return Text(f'population: {population}', (self.rect.centerx, 50), is_centered=True, font_size=24, color=style.black)
