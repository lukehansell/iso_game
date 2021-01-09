from .events import SELECT_TILE, DESELECT_TILE

def reducer(state, action):
    if action.type == SELECT_TILE:
        return action.tile

    if action.type == DESELECT_TILE:
        return None

    return state