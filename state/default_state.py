from camera import Camera

state = {
    "system": {
        "is_quitting": False,
        "is_fullscreen": False,
        "mouse_position": (0, 0)
    },
    "camera": Camera(100, 100),
    "selected_tile": None,
    "ui": {
        "popup": False
    }
}