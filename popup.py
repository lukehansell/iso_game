import pygame as py
class Popup(py.sprite.Sprite):
    def __init__(self, screen, title, content, position = (100, 100), onClose=None):
        py.sprite.Sprite.__init__(self, self.containers)
        popup_width = 300
        popup_height = 400
        popup_padding = 5

        popup_background = (100, 100, 100)

        surface = py.Surface((popup_width, popup_height))
        surface.fill(popup_background)

        button_height = 50
        button_width = popup_width - (2 * popup_padding)

        button_position = (
            popup_padding,
            popup_height - popup_padding - button_height
        )

        button_size = (button_width, button_height)

        self.ui = py.sprite.Group()
        Button.containers = self.ui

        self.close_button = Button('close', button_position, button_size, position, onClose)

        self.image = surface
        self.rect = surface.get_rect(topleft=position)

    def update(self, state):
        self.ui.update(state)
        self.ui.draw(self.image)

class Button(py.sprite.Sprite):
    color = (0, 116, 217)
    highlight_color = (51, 144, 225)

    def __init__(self, text, position, size, parentOffset=(0, 0), onClick = None):
        py.sprite.Sprite.__init__(self, self.containers)

        self.position = position

        self.image = py.Surface(size)
        self.rect = self.image.get_rect(topleft=position)
        self.parentOffset = parentOffset
        self.onClick = onClick

        small_text = py.font.Font(None, 20)
        self.ui = py.sprite.Group()
        Text.containers = self.ui

        self.text = Text(text, small_text)

    def update(self, state):

        mouse = py.mouse.get_pos()
        button_is_hovered = self.rect.topleft[0] + self.rect.width + self.parentOffset[0] > mouse[0] > self.parentOffset[0] + self.rect.topleft[0] and self.rect.topleft[1] + self.rect.height + self.parentOffset[1] > mouse[1] > self.rect.topleft[1] + self.parentOffset[1]

        color = self.highlight_color if button_is_hovered else self.color
        self.image.fill(color)

        self.ui.draw(self.image)

        if button_is_hovered and py.mouse.get_pressed()[0]:
            if self.onClick:
                self.onClick()

class Text(py.sprite.Sprite):
    def __init__(self, text, font, position=(0, 0)):
        py.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = text_objects(text, font, position)

def text_objects(text, font, position=(0,0)):
    print(text)
    text_surface = font.render(text, True, (255, 255, 255))
    return text_surface, text_surface.get_rect(topleft=position)
