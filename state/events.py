from pygame.event import Event, post, custom_type

SELECT_TILE = custom_type()
DESELECT_TILE = custom_type()

DISPLAY_SELECTED_TILE_POPUP = custom_type()
HIDE_SELECTED_TILE_POPUP = custom_type()

TOGGLE_FULLSCREEN = custom_type()

def create_select_tile_event(tile):
    post(Event(SELECT_TILE, { "tile": tile }))
    create_display_selected_tile_popup()

def create_deselect_tile_event():
    create_hide_selected_tile_popup()
    post(Event(DESELECT_TILE))

def create_display_selected_tile_popup():
    post(Event(DISPLAY_SELECTED_TILE_POPUP))

def create_hide_selected_tile_popup():
    post(Event(HIDE_SELECTED_TILE_POPUP))

def create_toggle_fullscreen():
    post(Event(TOGGLE_FULLSCREEN))