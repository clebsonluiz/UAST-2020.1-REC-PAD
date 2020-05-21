import pygame as pg

from ..layer import BackgroundMap
from ..entity import EntityMap


class FireDesintegrator(EntityMap):
    """
    Animated entity Fire Desintegrator to Kill Player if he not got coins
    """
    def __init__(self, background: BackgroundMap, invert_gravity: bool = False):
        super().__init__('Fire_by_Davias_100404.png',
                         background=background,
                         invert_gravity=invert_gravity)

    def get_animation_row(self) -> int:
        """
        :return: int value of a animation to be executed in event check
        """
        return 0

    def update(self):
        """
        update the current object
        """
        self.set_curr_row(curr_row=self.get_animation_row())
        super().super_update()

    def render(self, tela: pg.Surface, color: tuple = (255, 255, 255, 255), opacity: int = None):
        """
        render this object at screen frame (tela)

        :param tela: Surface of screen that object will be drawed
        :param color: tuple of primary color of image
        """
        if tela is None:
            return
        if color is not None:
            self.current_sprite().fill(color=color, special_flags=pg.BLEND_RGBA_MIN)
        self.invert_y = self._g_inverted
        image = pg.transform.flip(self.current_sprite(), not self.invert_x, self.invert_y,).convert()
        tela.blit(image, self.get_position())

    def make_animations_list(self):
        """
        build the list of animations of this entity
        """
        s_matrix = self.build(
            t_width=142, t_height=162,
            cols=5, rows=2,
            i_x=50, i_y=30,
            jmp_p_x=50, jmp_p_y=30
        )
        s_list = EntityMap.sprite_list(
            from_list=s_matrix,
            from_row=0, from_i=1, to_i=8,
        )
        self.insert(s_list)
        self._loaded = True
