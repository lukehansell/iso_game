from pygame.event import Event, post, custom_type

SELECT_TILE = custom_type()
DESELECT_TILE = custom_type()

DISPLAY_SELECTED_TILE_POPUP = custom_type()
HIDE_SELECTED_TILE_POPUP = custom_type()

DISPLAY_POPUP = custom_type()
HIDE_POPUP = custom_type()

TOGGLE_FULLSCREEN = custom_type()

def create_select_tile_event(tile):
    print('dispatching SELECT_TILE')
    post(Event(SELECT_TILE, { "tile": tile }))
    create_display_selected_tile_popup()

def create_deselect_tile_event():
    print('dispatching DESELECT_TILE')
    create_hide_selected_tile_popup()
    post(Event(DESELECT_TILE))

def create_display_selected_tile_popup():
    print('dispatching DISPLAY_SELECTED_TILE_POPUP')
    post(Event(DISPLAY_SELECTED_TILE_POPUP))

def create_hide_selected_tile_popup():
    print('dispatching HIDE_SELECTED_TILE_POPUP')
    post(Event(HIDE_SELECTED_TILE_POPUP))

def create_toggle_fullscreen():
    print('dispatching TOGGLE_FULLSCREEN')
    post(Event(TOGGLE_FULLSCREEN))

def create_display_popup(title, content):
    print('dispatching DISPLAY_POPUP')
    post(Event(DISPLAY_POPUP, { "title": title, "content": content }))

def create_hide_popup():
    print('dispatching HIDE_POPUP')
    post(Event(HIDE_POPUP))