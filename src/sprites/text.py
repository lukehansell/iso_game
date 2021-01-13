import pygame as py
import src.groups as groups

class Text(py.sprite.Sprite):
    def __init__(self, text, position=(0, 0), on_click=None, font_size=20, is_centered=False, layer=0, color=(255,255,255)):
        self._layer = layer
        font = py.font.Font(None, font_size)
        py.sprite.Sprite.__init__(self, (groups.all, groups.layeredItems, groups.overlays))
        self.image, self.rect = text_objects(text, font, position, is_centered, color)
        self.on_click = on_click


def text_objects(text, font, position=(0,0), is_centered=False, color=(255,255,255)):
    text_surface = font.render(text, True, color)
    if is_centered:
        return text_surface, text_surface.get_rect(center=position)

    return text_surface, text_surface.get_rect(topleft=position)