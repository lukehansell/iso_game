import pygame as py

class HoverableSprite(py.sprite.Sprite):
    '''Sprite with built in hover functionality

        Checks the hover state using the mouse position on update
        and calls on_hover with the state.
    '''
    def __init__(self, *args, **kwargs):
        print(args, kwargs)
        py.sprite.Sprite.__init__(self, *args, **kwargs)

    def update(self, *args, **kwargs):
        '''Update method checks mouse position for hover state

            Calls the `self.on_hover` method.
            If the mouse is within the sprite's rectangle it passes True else False
        '''
        mouse = py.mouse.get_pos()
        is_hovered = (
            (self.rect.topleft[0] + self.rect.width > mouse[0] > self.rect.topleft[0])
            and
            (self.rect.topleft[1] + self.rect.height > mouse[1] > self.rect.topleft[1])
        )
        self.on_hover(is_hovered)

    def on_hover(self, is_hovered):
        pass