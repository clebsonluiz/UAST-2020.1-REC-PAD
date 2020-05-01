from ..layer import BackgroundMap
from math import sqrt as raiz


class Sensor:
    """
    Sensor class, represents the one object sensor of a one player

    Parameters
    __________
    player: Player
        Player of the will be composed of that sensor and his atributes
    background: BackgroundMap
        Colision layer of the player object to get the obstacles
    """
    def __init__(self, player, background_map: BackgroundMap):
        from game.model.player import Player
        self.player: Player = player
        self.bg_map: BackgroundMap = background_map
        self._curr_shadow_distance_from_obstacle = 0
        self._curr_player_distance_from_obstacle = 0
        self._curr_speed = 0.0
        self._curr_width_of_first_obstacle = 0

    def get_center_pos_player(self) -> tuple:
        """
        :return: gets the tuple the pos x and y of center rect
        """
        return self.player.player.to_rect().center

    def get_center_pos_shadow(self) -> tuple:
        """
        :return: gets the tuple the pos x and y of center rect
        """
        return self.player.shadow.to_rect().center

    def get_first_obstacle(self):
        """
        :return: the first obstacle who is analised distance and size
        """
        curr_obs = self.bg_map.get_obstacles()[0]
        if curr_obs.to_rect().right < self.player.to_rect().left:
            curr_obs = self.bg_map.get_obstacles()[1]
        return curr_obs

    def update(self):
        """
        Updates the current atributes of this object in Player cass
        """
        obs = self.get_first_obstacle()

        self._curr_player_distance_from_obstacle = Sensor.calc_dist(
            self.get_center_pos_player(),
            obs.to_rect().center)
        self._curr_shadow_distance_from_obstacle = Sensor.calc_dist(
            self.get_center_pos_shadow(),
            obs.to_rect().center)

        self._curr_width_of_first_obstacle = obs.to_rect().width
        self._curr_speed = self.bg_map.get_curr_map_speed()

    def get_curr_width_of_obstacle(self):
        """
        :return: Current size width of the first obstacle
        """
        return self._curr_width_of_first_obstacle

    def get_curr_dist_shadow_to_obstacle(self):
        """
        :return: Current distance between shadow player and first obstacle
        """
        return self._curr_shadow_distance_from_obstacle

    def get_curr_dist_player_to_obstacle(self):
        """
        :return: Current distance between player and first obstacle
        """
        return self._curr_player_distance_from_obstacle

    def get_curr_speed(self):
        """
        :return: Current map speed
        """
        return self._curr_speed

    @staticmethod
    def calc_dist(pos1: tuple, pos2: tuple) -> float:
        """
        Calcs the distance between of two position vectors.
        √((x2 - x1)² + (y2 - y1)²)

        :return: Current distance between the pos1 and pos2
        """
        x1 = pos1[0]
        x2 = pos2[0]
        y1 = pos1[1]
        y2 = pos2[1]

        return raiz(((x1 - x2)**2) + ((y1 - y2)**2))
