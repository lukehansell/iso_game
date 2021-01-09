import pygame as py
class Popup():
    def __init__(self, screen, title, content):
        surface = py.Surface((300, 400))
        py.draw.rect(surface, (100, 100, 100), (0, 0, 300, 400))

        mouse = py.mouse.get_pos()

        if 25 + 250 + 100 > mouse[0] > 100 + 25 and 325 + 50 + 100 > mouse[1] > 325 + 100:
            # hovering
            button = py.draw.rect(surface, (50, 50, 255), (25, 325, 250, 50))
        else:
            button = py.draw.rect(surface, (0, 0, 255), (25, 325, 250, 50))

        small_text = py.font.Font(None, 20)
        text_surface, text_rect = text_objects("done", small_text)

        surface.blit(text_surface, button.center)
        screen.blit(surface, (100, 100))

def text_objects(text, font):
    text_surface = font.render(text, True, (255, 255, 255))
    return text_surface, text_surface.get_rect()