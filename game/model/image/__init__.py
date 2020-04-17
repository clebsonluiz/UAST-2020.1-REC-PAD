from .game_image import GameImage


def load(file: str) -> GameImage:

    """
    Loads a GameImage based in pygame.image
    and make the return from ASSETS_PATH + 'images/' + file: str name,

    :parameter file: str archive name with format like 'example.png'
    :return GameImage Class
    """
    assert file is not None and len(file) > 4
    from game.constants import ASSETS_PATH
    img: GameImage = GameImage(file=ASSETS_PATH + 'images/' + file)
    return img
