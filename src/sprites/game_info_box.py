import pygame as py
from src.groups import overlays, layeredItems, all as all_sprites

import src.style as style
from src.text.paragraph import P
from src.text.render import render
from src.lib.dates import int_to_short_month_name
from .text import Text
from functools import reduce

class GameInfoBox(py.sprite.Sprite):
    def __init__(self, position, layer=1, size=(350, 75)):
        py.sprite.Sprite.__init__(self, (all_sprites, overlays, layeredItems))

        self.position = position
        self._layer = layer

        (width, height) = size

        children_config = self.create_children()

        self.children = render(children_config, position=self.position)
        children_height = reduce(lambda acc, child: acc + child.rect.height, self.children, 0)
        width = size[0]
        height = children_height + style.padding * 2

        surface = py.Surface((width, height), py.SRCALPHA)

        py.draw.rect(
            surface,
            style.white,
            py.Rect(0, 0, width, height),
            border_bottom_left_radius=style.border_radius,
            border_bottom_right_radius=style.border_radius
        )

        self.image = surface
        self.rect = self.image.get_rect(midtop=position)

    def create_children(self, state = None):
        cash = '-' if not state else state['game']['balance']
        population = '-' if not state else state['game']['population']
        month = '-' if not state else int_to_short_month_name(state['game']['date']['month'])
        year = '-' if not state else state['game']['date']['year']

        return [
            P(
                f'cash balance: ${cash}',
                24
            ),
            P(
                f'population: {population}',
                16
            ),
            P(
                f'{month} / {year}',
                16
            )
        ]

    def update(self, state):
        for child in self.children:
            child.kill()

        children_config = self.create_children(state)
        self.children = render(children_config, position=self.position)

