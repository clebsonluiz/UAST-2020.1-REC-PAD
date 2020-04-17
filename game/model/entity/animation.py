from typing import List
import pygame as pg


class Animation:
    """
    Animation Class
    _______________
    Make a simple change of Sprites Frames during the update in game loop.
    Represents a list frames who pertences a current animation.

    Parameters
    __________
    frames : List[pg.SurfaceType]
        List of frames image to be animated
    loop : bool, optional
        If the frames list do a loop animation or not
    """
    def __init__(self, frames: List[pg.SurfaceType], loop: bool = True):
        assert frames is not None and loop is not None
        self.frames: List[pg.SurfaceType] = frames
        self.loop: bool = loop
        self._played: bool = False
        self._curr_col: int = 0

    def get_frame(self) -> pg.SurfaceType:
        """
        :return: current frame image from this animation
        """
        return self.frames[self._curr_col]

    def update(self):
        """
        Updates the animations, changing the current frame
        """
        if self._played:
            return
        self._curr_col += 1
        if self._curr_col >= len(self.frames):
            if self.loop:
                self.reset()
            else:
                self._curr_col = len(self.frames) - 1
                self._played = True

    def reset(self):
        """
        Resets the current animation and make changing
        of current frame to the first frame
        """
        self._curr_col = 0
        self._played = False
