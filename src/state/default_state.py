from src.camera import Camera

state = {
    "system": {
        "is_quitting": False,
        "is_fullscreen": False,
        "mouse_position": (0, 0)
    },
    "camera": Camera(100, 100),
    "selected_tile": None,
    "ui": {
        "popup": None
    },
    "build_mode": None,
    "game": {
        "speed": 0,
        "date": {
            'month': 1,
            'year': 2000
        },
        "balance": 1000000,
        "population": 0
    }
}