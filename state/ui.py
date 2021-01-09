from .events import DISPLAY_SELECTED_TILE_POPUP, HIDE_SELECTED_TILE_POPUP

def reducer(state, action):
    if action.type == DISPLAY_SELECTED_TILE_POPUP:
        return {
            "popup": True
        }

    if action.type == HIDE_SELECTED_TILE_POPUP:
        return {
            "popup": False
        }

    return state