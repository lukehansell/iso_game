import pygame as py
from camera import Camera
CAMERA_SPEED = 5

def reducer(state, action):
    if action.type == py.KEYDOWN:
        if action.key == py.K_LEFT:
            state.dx += CAMERA_SPEED
        if action.key == py.K_RIGHT:
            state.dx += -CAMERA_SPEED
        if action.key == py.K_UP:
            state.dy += CAMERA_SPEED
        if action.key == py.K_DOWN:
            state.dy += -CAMERA_SPEED

    if action.type == py.KEYUP:
        if action.key == py.K_LEFT:
            state.dx -= CAMERA_SPEED
        if action.key == py.K_RIGHT:
            state.dx -= -CAMERA_SPEED
        if action.key == py.K_UP:
            state.dy -= CAMERA_SPEED
        if action.key == py.K_DOWN:
            state.dy -= -CAMERA_SPEED

    return state