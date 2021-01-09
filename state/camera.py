import pygame as py
from camera import Camera
CAMERA_SPEED = 5

def reducer(state, action):
    keys = py.key.get_pressed()
    dx = (keys[py.K_LEFT] - keys[py.K_RIGHT]) * CAMERA_SPEED
    dy = (keys[py.K_UP] - keys[py.K_DOWN]) * CAMERA_SPEED

    state.update((dx, dy))
    return state