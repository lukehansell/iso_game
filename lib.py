def grid_ref_to_iso(point, x_offset=0, y_offset=0, height=18, width=32):
    (x, y) = point
    return (x_offset + (x * width) - (y * width), y_offset + (x * height) + (y * height) - 64)

def iso_to_grid_ref(point):
    (x, y) = point

    grid_x = ((18*x)+(32*y))/1152
    grid_y = (y - (18*grid_x))/18
    return (round(grid_x)-1, round(grid_y))