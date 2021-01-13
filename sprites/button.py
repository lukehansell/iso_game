import pygame as py
import groups
from sprites.text import Text

class Button(py.sprite.Sprite):
    color = (0, 116, 217)
    highlight_color = (51, 144, 225)

    def __init__(self, text, position, size, on_click = None, layer=2):
        py.sprite.Sprite.__init__(self, (groups.all, groups.layeredItems, groups.overlays))
        self._layer = layer
        self.position = position

        self.image = py.Surface(size)
        py.draw.rect(self.image, self.color, py.Rect(0, 0, size[0], size[1]), border_radius=10)
        self.rect = self.image.get_rect(topleft=position)
        self.on_click = on_click

        self.text = Text(text, self.rect.center, self.on_click, is_centered=True, layer=self._layer+1)

    def update(self, state):
        mouse = py.mouse.get_pos()
        button_is_hovered = self.rect.topleft[0] + self.rect.width > mouse[0] > self.rect.topleft[0] and self.rect.topleft[1] + self.rect.height > mouse[1] > self.rect.topleft[1]

        color = self.highlight_color if button_is_hovered else self.color
        py.draw.rect(self.image, color, py.Rect(0, 0, self.rect.width, self.rect.height), border_radius=10)

    def kill(self):
        self.text.kill()
        py.sprite.Sprite.kill(self)
