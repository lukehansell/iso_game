import src.style as style
from src.sprites.text import Text

def render(content, position=(0,0)):
    children = []
    (container_x_center, container_y) = position

    for item in content:
        y = container_y + style.padding * 3 if len(children) == 0 else children[-1].rect.bottom + style.padding * 2

        new_item = Text(
            item.text,
            (container_x_center, y),
            is_centered=True,
            font_size=item.font_size,
            color=style.black
        )
        children.append(new_item)
    return children