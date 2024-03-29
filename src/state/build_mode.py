from enum import Enum
from .events import TOGGLE_BUILD_MODE

class BUILD_MODES(Enum):
    RESIDENTIAL = 0
    COMMERCIAL = 1
    INDUSTRIAL = 2

def reducer(state, action):
    if action.type == TOGGLE_BUILD_MODE:
        if action.mode == state:
            return None
        else:
            return action.mode

    return state