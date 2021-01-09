from .system import reducer as systemReducer
from .camera import reducer as cameraReducer
from .selected_tile import reducer as selectedTileReducer
from .ui import reducer as uiReducer

def reducer(state, action):
    if action == None:
        return state

    return {
        "system": systemReducer(state['system'], action),
        "camera": cameraReducer(state['camera'], action),
        "selected_tile": selectedTileReducer(state['selected_tile'], action),
        "ui": uiReducer(state['ui'], action)
    }