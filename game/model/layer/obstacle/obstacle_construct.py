from typing import List
from random import randint as next_int

import pygame as pg

from .obstacle import Obstacle
from ..background import BackgroundLayers

from game.constants import \
    MATRIX_OBSTACLE_1_TOP, \
    MATRIX_OBSTACLE_2_TOP, \
    MATRIX_OBSTACLE_3_TOP, \
    MATRIX_OBSTACLE_1_BOTTOM, \
    MATRIX_OBSTACLE_2_BOTTOM, \
    MATRIX_OBSTACLE_3_BOTTOM, \
    SCREEN_WIDTH, WHITE, YELLOW, get_render_type


class ObstacleConstruct:
    """
    ObstacleConstruct Class
    _______________________
    Used to manage the obstacles on background layer and generate them

    Parameter :
        background_layers : BackgroundLayers
            BackgroundLayer when the obstacles is generated
    """

    def __init__(self, background_layers: BackgroundLayers = None):
        self._BACKGROUND_LAYERS: BackgroundLayers = background_layers
        self._OBSTACLES: List[Obstacle] = []
        self._top_obstacle_matrix_list = []
        self._bottom_obstacle_matrix_list = []
        self._lowest_dist: int = 200
        self._biggest_dist: int = 300
        self._top_or_bottom = None
        self._dificult_type = None
        self.set_dificult_type('easy')

    def _dificult_type_1(self):
        self._top_obstacle_matrix_list.append(
            MATRIX_OBSTACLE_1_TOP
        )
        self._bottom_obstacle_matrix_list.append(
            MATRIX_OBSTACLE_1_BOTTOM
        )
        self._lowest_dist: int = 300
        self._biggest_dist: int = 500
        self._top_or_bottom = [False, True]
        self._dificult_type = 'easy'

    def _dificult_type_2(self):
        self._top_obstacle_matrix_list.append(
            MATRIX_OBSTACLE_2_TOP
        )
        self._bottom_obstacle_matrix_list.append(
            MATRIX_OBSTACLE_2_BOTTOM
        )
        self._lowest_dist: int = 350
        self._biggest_dist: int = 600
        self._top_or_bottom = [False, True]
        self._dificult_type = 'normal'

    def _dificult_type_3(self):
        self._top_obstacle_matrix_list.append(
            MATRIX_OBSTACLE_3_TOP
        )
        self._bottom_obstacle_matrix_list.append(
            MATRIX_OBSTACLE_3_BOTTOM
        )
        self._lowest_dist: int = 500
        self._biggest_dist: int = 800
        self._top_or_bottom = [False, True]
        self._dificult_type = 'hard'

    def set_dificult_type(self, dificult: str):
        if dificult is self._dificult_type:
            return
        if dificult == 'easy':
            self._dificult_type_1()
        elif dificult == 'normal':
            self._dificult_type_2()
        elif dificult == 'hard':
            self._dificult_type_3()

    def _generate_distance(self, firsts: bool = False) -> int:
        """
        Generate the distance between obstacles

        :return: the int distance in x axis
        """
        if firsts:
            dist = self._lowest_dist
        else:
            dist = next_int(self._lowest_dist, self._biggest_dist)  # Gerar uma distãncia entre obstaculos
        if len(self._OBSTACLES) != 0:
            return self._OBSTACLES[-1].get_last_distance(default=dist)
        return SCREEN_WIDTH

    def _generate_matrix_tile(self, position_up: bool = False) -> List[List[float]]:
        """
        Chooses a matrix to build the image of the obstacle

        :param position_up: if the matrix is a top matrix
        :return: the matrix List[List[float]]
        """
        limit = len(self._top_obstacle_matrix_list) + len(self._bottom_obstacle_matrix_list)
        index: int = next_int(0, int((limit / 2) - 1))
        if position_up:
            return self._top_obstacle_matrix_list[index]
        return self._bottom_obstacle_matrix_list[index]

    def _generate_obstacle(self, position_up: bool = False, firsts: bool = False) -> Obstacle:
        """
        Generates a new Obstacle

        :param position_up: if the obstacle is on top obstacle or not
        :return: the new Obstacle
        """
        obs: Obstacle = Obstacle(
            self._generate_matrix_tile(position_up),
            self.get_bg_layers(),
            dx=-1.0, dy=0.0,
        )
        obs.pos_x = self._generate_distance(firsts=firsts)
        obs.pos_y = obs.my_relative_positon_on_map(position_up)
        obs.set_colision_padding(
            pg.Rect(0.0, -20.0 if position_up else -25.0, 0.0, 64.0)
        )
        obs.build_coin(position_up=position_up)
        return obs

    def get_obstacles(self) -> List[Obstacle]:
        """
        :return: gets the obstacles list
        """
        return self._OBSTACLES

    def get_bg_layers(self):
        """
        :return: the background layers class object used to build the obstacles
        """
        return self._BACKGROUND_LAYERS

    def set_bg_layers(self, background_layers):
        """
        Sets the background layers if the is not set on constructor

        :param background_layers: BackgroundLayers
        """
        if self._BACKGROUND_LAYERS or background_layers is None:
            return
        self._BACKGROUND_LAYERS = background_layers

    def generate(self, bg_layers: BackgroundLayers,
                 firsts: bool = False) -> List[Obstacle]:
        """
        Generate the obstacle ant put it on the list of obstacles

        :param bg_layers: BackgroundLayers object
        :param firsts: if the obstacles is the first three positions
        :return: list of obstacles atualized
        """
        self.set_bg_layers(bg_layers)
        if firsts:
            self.get_obstacles().clear()
            self.get_obstacles().append(self._generate_obstacle(firsts=firsts))
            self.get_obstacles().append(self._generate_obstacle(position_up=True, firsts=firsts))
            self.get_obstacles().append(self._generate_obstacle(firsts=firsts))

        self._OBSTACLES.append(
            self._generate_obstacle(self._top_or_bottom[next_int(0, 1)])
        )
        return self._OBSTACLES

    def update(self, speed: float = 1.0):
        """
        Updates the list of obstacles and yours currents positions

        :param speed: movement speed of the obstacles
        """
        obstacles = self.get_obstacles()
        if len(self.get_obstacles()) == 0:
            return
        if len(obstacles) <= 4:
            self.generate(self.get_bg_layers())
        if obstacles[0].is_out_screen():
            obstacles.pop(0)
        for e in obstacles:
            e.update(speed=speed)

    def render(self, tela: pg.Surface):
        """
        Render the obstacles on Surface

        :param tela: pygame Surface when the obstacles are drawed in
        """
        if tela:
            for e in self.get_obstacles():
                if get_render_type().get('COLISION'):
                    tela.fill(WHITE, e.to_rect())
                    if e.coin_still_in_obstacle():
                        tela.fill(YELLOW, e.get_coin().to_rect())
                if get_render_type().get('NORMAL'):
                    e.render(tela=tela)

    def reset(self):
        self._dificult_type = None
        self._top_obstacle_matrix_list.clear()
        self._bottom_obstacle_matrix_list.clear()
        self.set_dificult_type('easy')
        self.generate(self.get_bg_layers(), firsts=True)

