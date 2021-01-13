from .events import PURCHASE, GAME_TICK
from functools import reduce

def reducer(state, action):
    if action.type == PURCHASE:
        new_state = state.copy()
        new_state['balance'] = state['balance'] - action.cost
        return new_state

    if action.type == GAME_TICK:
        for tile in action.tiles:
            tile.game_tick()

        profit = reduce(calc_profit, action.tiles, 0)
        new_state = state.copy()
        new_state['balance'] = state['balance'] + profit
        return new_state

    return state

def calc_profit(acc, tile):
    return acc + tile.stats.population * 10 #TODO make variable on tax rate