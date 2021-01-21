import pygame as py
import src.groups as groups
import src.style as style

from .text import Text
from .button import Button, ButtonType, CloseButton

class Popup(py.sprite.Sprite):
    def __init__(self,
        content = py.Surface((0 ,0)),
        title = None,
        position = (150, 150),
        on_close = None,
        layer = 99
    ):
        py.sprite.Sprite.__init__(self, (groups.all, groups.layeredItems, groups.overlays))
        popup_width = 300
        popup_height = 400
        popup_padding = style.padding

        surface = py.Surface((popup_width, popup_height), py.SRCALPHA)
        py.draw.rect(
            surface,
            style.primary_color,
            py.Rect(0, 0, popup_width, popup_height),
            border_radius=style.border_radius
        )
        py.draw.rect(
            surface,
            style.white,
            py.Rect(
                popup_padding,
                popup_padding,
                popup_width-popup_padding*2,
                popup_height-popup_padding*2
            ),
            border_radius=style.border_radius
        )

        button_position = (
            position[0] + popup_width - popup_padding*4,
            position[1] + popup_padding*4
        )

        self._layer = layer

        if title is not None:
            title_position = (
                position[0] + popup_padding,
                position[1] + popup_padding
            )

            self.title = Text(
                title,
                title_position,
                font_size=32,
                layer=self._layer + 1,
                color=style.black
            )

        self.close_button = CloseButton(
            button_position,
            on_close,
            layer=self._layer+1,
            color=style.primary_color
        )

        surface.blit(content, (popup_padding, popup_padding + 30))
        self.image = surface
        self.rect = surface.get_rect(topleft=position)

    def kill(self):
        self.title.kill()
        self.close_button.kill()
        py.sprite.Sprite.kill(self)
