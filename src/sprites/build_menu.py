import pygame as py
from functools import reduce

import src.groups as groups
import src.style as style

from .text import Text
from .hoverable_sprite import HoverableSprite
from ..state.build_mode import BUILD_MODES

class BuildMenu(py.sprite.Sprite):
    width = 300
    height = 400
    padding = 5

    background = style.primary_color

    def __init__(self, height, width=60, position = (0, 0), on_build_option_select=None, layer=30):
        py.sprite.Sprite.__init__(self, (groups.all, groups.layeredItems, groups.overlays))

        (container_x, container_y) = position
        title_x = container_x + style.padding
        title_y = container_y + style.padding
        self._layer = layer
        self.title = Text(
            'Build Modes:',
            (title_x, title_y)
        )
        build_mode_items = {
            'Residential': BUILD_MODES.RESIDENTIAL,
            'Commercial': BUILD_MODES.COMMERCIAL,
            'Industrial': BUILD_MODES.INDUSTRIAL,
        }

        self.menu = Menu(
            build_mode_items,
            on_build_option_select,
            (container_x + style.padding, self.title.rect.bottom + style.padding))

        height = self.title.rect.height + self.menu.rect.height + self.padding*2

        self.image = py.Surface((width, height), py.SRCALPHA)
        self.image.fill(self.background)
        self.rect = self.image.get_rect(topleft=position)

    def update(self, state):
        for option in self.menu.menu_items:
            is_active = True if state['build_mode'] == option.value else False
            option.set_active(is_active)

    def kill(self):
        py.sprite.Sprite.kill(self)

class MenuItem(HoverableSprite):
    def __init__(self, text, value, on_click, position=(0, 0), layer=1, is_active=False):
        HoverableSprite.__init__(self, (groups.all, groups.layeredItems, groups.overlays))
        self._layer = layer
        self.handle_click = on_click
        self.value = value
        self.is_active = is_active

        self.is_hovered = False
        self.is_active = False

        (text_x, text_y) = position
        self.text = Text(
            text,
            (
                text_x + style.padding,
                text_y + style.padding
            ),
            color=style.menu_item_text,
            on_click=self.on_click
        )
        (text_width, text_height) = self.text.image.get_size()
        width = text_width + style.padding*2
        height = text_height + style.padding*2

        self.image = py.Surface((width, height), py.SRCALPHA)
        self.image.fill(style.white)
        self.rect = self.image.get_rect(topleft=position)

    def on_hover(self, is_hovered):
        self.is_hovered = is_hovered
        if is_hovered:
            self.image.fill(style.menu_item_hovered)
        else:
            if not self.is_active:
                self.image.fill(style.menu_item)

    def on_click(self):
        self.handle_click(self.value)

    def set_active(self, is_active):
        self.is_active = is_active
        if is_active:
            self.image.fill(style.menu_item_hovered)
        else:
            self.image.fill(style.menu_item)



class Menu(py.sprite.Sprite):
    def __init__(self, options, on_item_click, position=(0, 0), layer=1):
        py.sprite.Sprite.__init__(self, (groups.all, groups.layeredItems, groups.overlays))
        self._layer=layer

        (container_x, container_y) = position

        self.menu_items = []

        x = container_x
        y = container_y
        for text, value in options.items():
            new_item = MenuItem(
                text,
                value,
                on_click=on_item_click,
                position=(x, y),
                layer=self._layer + 1
            )
            self.menu_items.append(new_item)
            x = new_item.rect.right + style.padding

        width = reduce(lambda acc, option: acc + option.rect.width, self.menu_items, 0)
        height = reduce(lambda acc, option: acc if acc > option.rect.height else option.rect.height, self.menu_items, 0)

        self.image = py.Surface((width, height), py.SRCALPHA)
        self.rect = self.image.get_rect()

    def set_active_item(self, value):
        for option in self.menu_items:
            is_active = True if value == option.value else False
            option.set_active(is_active)
