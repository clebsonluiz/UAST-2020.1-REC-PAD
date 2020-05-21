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
        :return: 1 / (1 + e^-t) if t >= 0 else return 1 - 1 / (1 + exp(t)) to not raise a OverflowError
        """
        from math import exp
        if t < 0:
            return 1 - 1 / (1 + exp(t))
        return 1 / (1 + exp(-t))

    @staticmethod
    def conditional(matrix, value):
        return lambda r: matrix[r][0] > value


class RedeNeural:

    def __init__(self, individuo):
        from ._individuo import Individuo
        self._individuo: Individuo = individuo
        self.BIAS = 1.0
        self.INPUT_RENDERS = [
            [False, False, False, False],
            [False, False],
            [False, False],
        ]

    def get_input_renders(self):
        return self.INPUT_RENDERS

    def reset_input_renders(self):
        R = self.INPUT_RENDERS
        R[0][0] = False
        R[0][1] = False
        R[0][2] = False
        R[0][3] = False
        R[1][0] = False
        R[1][1] = False
        R[2][0] = False
        R[2][1] = False

    def get_entradas_matrix(self) -> Matrix:
        return Matrix([
            [self._individuo.get_sensor().get_curr_dist_shadow_to_obstacle()],
            [self._individuo.get_sensor().get_curr_dist_player_to_obstacle()],
            [self._individuo.get_sensor().get_curr_width_of_obstacle()],
            [self._individuo.get_sensor().get_curr_speed()]
        ])

    def _gene(self, key):
        return self._individuo.cromossomo[key]

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
            [self._gene('GF01'), self._gene('GF11'), self._gene('GF21')],
            [self._gene('GF02'), self._gene('GF12'), self._gene('GF22')],
        ])

    def get_individuo(self):
        return self._individuo

    def update(self):
        """
        """
        self.reset_input_renders()
        # Camada de Entradas da rede neural junto com o viés BIAS
        entradas: Matrix = self.get_entradas_matrix()
        entradas.get().insert(0, [self.BIAS])

        R = self.INPUT_RENDERS
        R[0][0] = True
        R[0][1] = True
        R[0][2] = True
        R[0][3] = True

        # Pesos da camada de entrada e da camada oculta
        pesos_entradas: Matrix = self.get_pesos_entradas_matrix()
        pesos_oculta: Matrix = self.get_pesos_neurais_matrix()

        # Camada oculta, OCULTA = ENTRADAS * PESOS_ENTRADAS da rede neural junto com o viés BIAS
        oculta: Matrix = pesos_entradas.mult(entradas)

        oculta.get().insert(0, [self.BIAS])
        # Função de Ativação usada para atualizar os valores
        oculta.map(_FuncaoAtivacao.sigmoid)

        R[1][0] = True
        R[1][1] = True

        # Camada de saida, SAIDA = OCULTA * PESOS_OCULTA
        saida: Matrix = pesos_oculta.mult(oculta)
        # Aplicação da Função de Ativação
        saida.map(_FuncaoAtivacao.sigmoid)

        # Execução da função de ativação, se usada a sigmoid logo valor da entrada deve ser maior que 0.5
        fa = _FuncaoAtivacao.conditional(saida.get(), 0.5)

        R[1][0] = fa(r=0)
        R[1][1] = fa(r=1)

        if fa(r=0):
            self._individuo.do_jump()
            R[1][0] = True
            R[2][0] = True
        if fa(r=1):
            self._individuo.do_change_gravit()
            R[1][1] = True
            R[2][1] = True

    @staticmethod
    def anulator_negatives(matrix: Matrix):
        for i in range(len(matrix.get())):
            for j in range(len(matrix.get()[i])):
                if matrix.get()[i][j] < 0:
                    matrix.get()[i][j] = 0
