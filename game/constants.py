import os
from typing import Dict

ASSETS_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/assets/"

# Colors
BLACK = (0, 0, 0, 255)
DARK_GRAY = (20, 20, 20, 255)
GRAY = (80, 80, 80, 255)
LIGTH_GRAY = (160, 160, 160, 255)
WHITE = (255, 255, 255, 255)
BLUE = (0, 0, 255, 255)
GREEN = (0, 255, 0, 255)
RED = (255, 0, 0, 255)
YELLOW = (255, 255, 0, 255)


"""
Color will be used to make the impression 
of the layer is bigger than realy is, only a 
thing to be more style and not ugle for diferent contrast 
color of the background and tile layer ¯\\_(ツ)_/¯
"""
DARK_SIDE_TILE_MAP = (20, 12, 28, 255)

BACKGROUND_COLOR = DARK_SIDE_TILE_MAP

# Screen dimensions
SCREEN_WIDTH = 32 * 20
SCREEN_HEIGHT = 32 * 15

# Builds Matrix of tiles
MATRIX_BACKGROUND_LAYER = [
    [19 for j0 in range(20)] for i0 in range(5)
]

MATRIX_LAYER_1 = [
    [1 for i1 in range(20)],
    # [17 for m1 in range(20)] # Only if the background color is not the DARK_SIDE_TILE_MAP color
]

MATRIX_LAYER_2 = [
    [1], [9], [9], [9], [9]
]

# MATRIX_LAYER_3 = [
#     [19],
#     [19],
#     [19],
#     [19],
#     [19],
#     [19],
#     [19],
#     [19]
# ]

MATRIX_OBSTACLE_1_BOTTOM = [
    [-23], [4], [6],
]

MATRIX_OBSTACLE_2_BOTTOM = [
    [-23, -23], [0, 2], [7, 5],
]

MATRIX_OBSTACLE_3_BOTTOM = [
    [-23, -23, -23], [0, 1, 2], [7, 9, 5]
]

MATRIX_OBSTACLE_1_TOP = [
    [-6], [-4], [23],
]

MATRIX_OBSTACLE_2_TOP = [
    [-7, -5], [16, 18], [23, 23],
]

MATRIX_OBSTACLE_3_TOP = [
    [-7, 9, -5], [16, 17, 18], [23, 23, 23],
]

_RENDER_LIST_TYPE = {
    'NORMAL': True,
    'DEBUG': False,
    'COLISION': False,
    'NEURAL': False,
}


def set_render_type(values: Dict[str, bool]):
    for e in values:
        b: bool = values[e]
        if get_render_type().get(e) is not None:
            get_render_type()[e] = b


def get_render_type() -> Dict[str, bool]:
    return _RENDER_LIST_TYPE
