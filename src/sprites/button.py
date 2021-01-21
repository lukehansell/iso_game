import pygame as py
from enum import Enum
import src.groups as groups
import src.style as style
from .text import Text
from .hoverable_sprite import HoverableSprite

class ButtonType(Enum):
    DEFAULT = 'default'
    WARNING = 'warning'

class Button(HoverableSprite):
    def __init__(
        self,
        text,
        position,
        on_click = None,
        layer=2,
        filled=False,
        type=ButtonType.DEFAULT
    ):
        HoverableSprite.__init__(self, (groups.all, groups.layeredItems, groups.overlays))

        if type == ButtonType.DEFAULT:
            self.color = (0, 116, 217)
            self.highlight_color = (51, 144, 225)
        elif type ==ButtonType.WARNING:
            self.color = (255, 65, 54)
            self.highlight_color = (255, 157, 152)

        self._layer = layer
        self.position = position
        self.on_click = on_click
        self.filled = filled

        self.text = Text(text, position, self.on_click, is_centered=True, layer=self._layer+1)

        self.image = py.Surface(self.text.rect.size, py.SRCALPHA)
        self.rect = self.image.get_rect(topleft=position)

        if filled:
            py.draw.rect(self.image, (92, 166, 231), py.Rect(0, 0, self.text.rect.width, self.text.rect.height), border_radius=style.border_radius)
            py.draw.rect(self.image, self.color, py.Rect(0, 0, self.text.rect.width, self.text.rect.height-style.border_radius), border_radius=style.border_radius)


    def on_hover(self, is_hovered):
        if self.filled:
            color = self.highlight_color if is_hovered else self.color
            py.draw.rect(self.image, color, py.Rect(0, 0, self.rect.width, self.rect.height), border_radius=style.border_radius)

    def kill(self):
        self.text.kill()
        py.sprite.Sprite.kill(self)

class CloseButton(Button):
    def __init__(self, position, on_click, layer=31, color=style.black):
        Button.__init__(self, '×', position, on_click=on_click, layer=layer)
        self.text.kill()
        self.text = Text('×', position, on_click, is_centered=True, font_size=64, color=color)
