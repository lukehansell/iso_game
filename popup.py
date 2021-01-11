import pygame as py
import groups

class Popup(py.sprite.Sprite):
    _layer = 1

    def __init__(self, content, title=None, position = (100, 100), on_close=None):
        py.sprite.Sprite.__init__(self, (groups.all, groups.layeredItems, groups.overlays))
        popup_width = 300
        popup_height = 400
        popup_padding = 5

        popup_background = (100, 100, 100)

        surface = py.Surface((popup_width, popup_height))
        surface.fill(popup_background)

        button_height = 25
        button_width = 25

        button_position = (
            position[0] + popup_width - popup_padding - button_width,
            position[1] + popup_padding
        )

        button_size = (button_width, button_height)

        if title is not None:
            title_position = (
                position[0] + popup_padding,
                position[1] + popup_padding
            )

            self.title = Text(title, title_position, font_size=32)

        self.close_button = Button('X', button_position, button_size, on_close)

        self.image = surface
        self.rect = surface.get_rect(topleft=position)

    def kill(self):
        self.title.kill()
        self.close_button.kill()
        py.sprite.Sprite.kill(self)

class Button(py.sprite.Sprite):
    _layer = 2
    color = (0, 116, 217)
    highlight_color = (51, 144, 225)

    def __init__(self, text, position, size, on_click = None):
        py.sprite.Sprite.__init__(self, (groups.all, groups.layeredItems, groups.overlays))

        self.position = position

        self.image = py.Surface(size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=position)
        self.on_click = on_click

        self.text = Text(text, self.rect.center, self.on_click, is_centered=True)

    def update(self, state):
        mouse = py.mouse.get_pos()
        button_is_hovered = self.rect.topleft[0] + self.rect.width > mouse[0] > self.rect.topleft[0] and self.rect.topleft[1] + self.rect.height > mouse[1] > self.rect.topleft[1]

        color = self.highlight_color if button_is_hovered else self.color
        self.image.fill(color)

    def kill(self):
        self.text.kill()
        py.sprite.Sprite.kill(self)

class Text(py.sprite.Sprite):
    _layer = 4

    def __init__(self, text, position=(0, 0), on_click=None, font_size=20, is_centered=False):
        font = py.font.Font(None, font_size)
        py.sprite.Sprite.__init__(self, (groups.all, groups.layeredItems, groups.overlays))
        self.image, self.rect = text_objects(text, font, position, is_centered)
        self.on_click = on_click


def text_objects(text, font, position=(0,0), is_centered=False):
    text_surface = font.render(text, True, (255, 255, 255))
    if is_centered:
        return text_surface, text_surface.get_rect(center=position)

    return text_surface, text_surface.get_rect(topleft=position)
