from typing import Dict
from ._matrix import Matrix


class _FuncaoAtivacao:

    @staticmethod
    def degrau(u):
        return 1 if u >= 0 else 0

    @staticmethod
    def degrau_bipolar(u):
        if u > 0:
            return 1
        elif u < 0:
            return -1
        return 0

    @staticmethod
    def sigmoid(t):
        """
        :param t:
        :return: 1 / (1 + e^-t)
        """
        from math import exp
        return 1 / (1 + exp(-t))


class RedeNeural:

    def __init__(self, individuo):
        from ._individuo import Individuo
        from ..model.player.sensor import Sensor
        self._individuo: Individuo = individuo
        self._sensor: Sensor = individuo.get_sensor()
        self._cromossomo: Dict = individuo.cromossomo
        self.BIAS = 1.0

    def get_entradas_matrix(self) -> Matrix:
        return Matrix([
            [self.BIAS],
            [self._sensor.get_curr_dist_shadow_to_obstacle()],
            [self._sensor.get_curr_dist_player_to_obstacle()],
            [self._sensor.get_curr_width_of_obstacle()],
            [self._sensor.get_curr_speed()]
        ])

    def _gene(self, key):
        return self._cromossomo[key]

    def get_pesos_entradas_matrix(self) -> Matrix:
        return Matrix([
            [
                self._gene('GN01'),
                self._gene('GN11'),
                self._gene('GN21'),
                self._gene('GN31'),
                self._gene('GN41')
            ],
            [
                self._gene('GN02'),
                self._gene('GN12'),
                self._gene('GN22'),
                self._gene('GN32'),
                self._gene('GN42')
            ],
        ])

    def get_pesos_neurais_matrix(self) -> Matrix:
        return Matrix([
            [self._gene('GF01'), self._gene('GF11')],
            [self._gene('GF02'), self._gene('GF12')],
        ])

    def get_individuo(self):
        return self._individuo

    def action(self):

        entradas: Matrix = self.get_entradas_matrix()
        pesos_entradas: Matrix = self.get_pesos_entradas_matrix()
        pesos_oculta: Matrix = self.get_pesos_neurais_matrix()

        oculta: Matrix = pesos_entradas.mult(entradas)
        RedeNeural.anulator_negatives(oculta)
        saida: Matrix = pesos_oculta.mult(oculta)

        u_1 = saida.get()[0][0]
        u_2 = saida.get()[1][0]

        if _FuncaoAtivacao.degrau(u_1):
            self._individuo.do_jump()
        if _FuncaoAtivacao.degrau(u_2):
            self._individuo.do_change_gravit()

    @staticmethod
    def anulator_negatives(matrix: Matrix):
        for i in range(len(matrix.get())):
            for j in range(len(matrix.get()[i])):
                if matrix.get()[i][j] < 0:
                    matrix.get()[i][j] = 0
