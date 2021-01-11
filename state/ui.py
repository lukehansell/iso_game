import pygame as py
from .events import DISPLAY_POPUP, HIDE_POPUP

def reducer(state, action):
    if action.type == py.MOUSEBUTTONDOWN:
        pass

    if action.type == DISPLAY_POPUP:
        return {
            "popup": {
                "title": action.title,
                "content": action.content
            }
        }

    if action.type == HIDE_POPUP:
        return {
            "popup": None
        }

    return state