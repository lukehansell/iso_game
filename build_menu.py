import pygame as py
import groups
from text import Text
from state.build_mode import BUILD_MODES

class BuildMenu(py.sprite.Sprite):
    width = 300
    height = 400
    padding = 5

    background = (255, 255, 255)

    def __init__(self, height, width=60, position = (0, 0), on_build_option_select=None, layer=30):
        py.sprite.Sprite.__init__(self, (groups.all, groups.layeredItems, groups.overlays))

        self._layer = layer

        surface = py.Surface((width, height))
        surface.fill(self.background)
        surface.set_alpha(100)

        self.image = surface
        self.rect = surface.get_rect(topleft=position)

        self.build_menu_items = {
            "Residential": BuildMenuItem(
                'R',
                (74,134,232),
                ( self.rect.left + self.padding, self.rect.top + self.padding ),
                False,
                BUILD_MODES.RESIDENTIAL,
                on_click=on_build_option_select,
                layer=self._layer + 1
            )
        }

    def update(self, state):
        for key in self.build_menu_items:
            is_active = True if state['build_mode'] == self.build_menu_items[key].build_mode else False
            self.build_menu_items[key].set_active(is_active)


    def kill(self):
        py.sprite.Sprite.kill(self)

class BuildMenuItem(py.sprite.Sprite):
    def __init__(self, text, color, position, is_active, build_mode, on_click=None, layer=31):
        py.sprite.Sprite.__init__(self, (groups.all, groups.layeredItems, groups.overlays))

        width = 50
        height = 50

        background_color = (255, 220, 0) if is_active else (255,255,255)

        self.build_mode = build_mode
        self.is_active = is_active
        self._layer = layer
        surface = py.Surface((width, height))
        self.border = py.draw.rect(surface, color, py.Rect(0, 0, 50, 50), border_radius=10)
        self.background = py.draw.rect(surface, background_color, py.Rect(5, 5, 40, 40), border_radius=10)

        self.handle_click = on_click
        self.text = Text(text, (25, 25), color=color, on_click=self.on_click)
        self.image = surface
        self.rect = surface.get_rect(topleft=position)

    def on_click(self):
        if self.handle_click is not None:
            self.handle_click(self.build_mode)

    def set_active(self, is_active):
        self.is_active = is_active
        color = (255, 220, 0) if is_active else (255,255,255)
        py.draw.rect(self.image, color, py.Rect(5, 5, 40, 40), border_radius=10)