import pygame as py

from .events import TOGGLE_FULLSCREEN

def reducer(state, action):
    return {
        "is_quitting": is_quitting_reducer(state.get('is_quitting'), action),
        "is_fullscreen": is_fullscreen_reducer(state.get('is_fullscreen'), action),
        "mouse_position": mouse_position_reducer(state.get('mouse_position'), action)
    }

def is_quitting_reducer(state, action):
    if action.type == py.QUIT:
        return True

    if action.type == py.KEYDOWN and action.key == py.K_ESCAPE:
        return True

    return state

def mouse_position_reducer(state, action):
    if action.type == py.MOUSEMOTION:
        return action.pos

    return state

def is_fullscreen_reducer(state, action):
    if action.type == py.KEYDOWN and action.key == py.K_f:
        return not state

    return state