import pygame as py
import src.groups as groups
import src.style as style

from .text import Text
from .button import Button

class Popup(py.sprite.Sprite):
    def __init__(self, content = py.Surface((0 ,0)), title=None, position = (100, 100), on_close=None, layer=60):
        py.sprite.Sprite.__init__(self, (groups.all, groups.layeredItems, groups.overlays))
        popup_width = 300
        popup_height = 400
        popup_padding = 10

        popup_background = style.dark_accent

        surface = py.Surface((popup_width, popup_height), py.SRCALPHA)
        py.draw.rect(surface, popup_background, py.Rect(0, 0, popup_width, popup_height), border_radius=style.border_radius)

        button_height = 25
        button_width = 25

        button_position = (
            position[0] + popup_width - popup_padding - button_width,
            position[1] + popup_padding
        )

        button_size = (button_width, button_height)

        self._layer = layer

        if title is not None:
            title_position = (
                position[0] + popup_padding,
                position[1] + popup_padding
            )

            self.title = Text(title, title_position, font_size=32, layer=self._layer + 1, color=style.white)

        self.close_button = Button('X', button_position, button_size, on_close, layer=self._layer+1)

        surface.blit(content, (popup_padding, popup_padding + 30))
        self.image = surface
        self.rect = surface.get_rect(topleft=position)

    def kill(self):
        self.title.kill()
        self.close_button.kill()
        py.sprite.Sprite.kill(self)
