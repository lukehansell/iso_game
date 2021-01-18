import pygame as py
import src.groups as groups
import src.style as style
from .text import Text
from .hoverable_sprite import HoverableSprite

class Button(HoverableSprite):
    color = (0, 116, 217)
    highlight_color = (51, 144, 225)

    def __init__(self, text, position, size, on_click = None, layer=2):
        HoverableSprite.__init__(self, (groups.all, groups.layeredItems, groups.overlays))
        self._layer = layer
        self.position = position

        self.image = py.Surface(size, py.SRCALPHA)
        py.draw.rect(self.image, self.color, py.Rect(0, 0, size[0], size[1]), border_radius=10)
        self.rect = self.image.get_rect(topleft=position)
        self.on_click = on_click

        self.text = Text(text, self.rect.center, self.on_click, is_centered=True, layer=self._layer+1)

    def on_hover(self, is_hovered):
        color = self.highlight_color if is_hovered else self.color
        py.draw.rect(self.image, color, py.Rect(0, 0, self.rect.width, self.rect.height), border_radius=style.border_radius)

    def kill(self):
        self.text.kill()
        py.sprite.Sprite.kill(self)
