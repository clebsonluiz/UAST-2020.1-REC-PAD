from typing import List
from ._individuo import Individuo


class Geracao:
    """
    Class who represents the Natural Selection Algoritm

    Parameters
    __________
    qtd_individuos: int
        Number of players how will compose one Generation
    o_melhor: Individuo
        Best default Player of the will be integrate to initial Generation
    o_atual: Individuo
        Default Current Player of the will be integrate to initial Generation
    """
    def __init__(self,
                 qtd_individuos: int = 1,
                 o_melhor: Individuo = None,
                 o_atual: Individuo = None,
                 ):
        from game.model.layer import BackgroundMap
        self.BG_MAP: BackgroundMap = BackgroundMap()
        self.MAX_POPULACAO: int = qtd_individuos
        self.POPULACAO: List[Individuo] = []
        self.O_MELHOR: Individuo = o_melhor
        self.O_ATUAL: Individuo = o_atual
        self.TAXA_MUTACAO: float = 0.25
        self._loaded: bool = False

    def is_loaded(self):
        """
        :return: True if the generation is loaded
        """
        if self.O_ATUAL is None or self.BG_MAP is None:
            return False
        return self._loaded and self.O_ATUAL.loaded()

    def atualiza_o_atual(self):
        """
        Updates the Current Player will play
        """
        if len(self.POPULACAO) <= 0:
            return
        self.O_ATUAL = self.POPULACAO[0]
        self.POPULACAO.pop(0)

    def seleciona_o_melhor(self):
        """
        Updates the best player
        :return: the Best Player
        """
        if self.O_ATUAL.get_score() > self.O_MELHOR.get_score():
            self.O_MELHOR = self.O_ATUAL
        return self.O_MELHOR

    def seleciona_populacao_inicial(self):
        """
        Select the initial population of the Generation
        """
        if self.O_MELHOR is None or self.O_ATUAL is None:
            self.O_ATUAL = Individuo.load_from_file(self.BG_MAP)
            self.O_MELHOR = self.O_ATUAL
        if self.O_ATUAL.cromossomo is None:
            self.O_ATUAL.create_cromossomo(randomize=True)
        self.seleciona_populacao(firsts=True)

    def seleciona_populacao(self, firsts: bool = False):
        """
        Generate the population of players

        :param firsts: if this population is the first, so will generate the genome
        """
        self.O_MELHOR.numero = 0
        self.O_MELHOR.geracao = self.O_MELHOR.geracao + 1
        self.POPULACAO.append(self.O_MELHOR)
        for i in range(self.MAX_POPULACAO - 1):
            individuo: Individuo = self.O_MELHOR.clone()
            individuo.numero = i + 1
            individuo.geracao = individuo.geracao + 1
            if firsts:
                individuo.cromossomo = individuo.create_cromossomo(randomize=True)
            else:
                individuo.mutation(taxa=self.TAXA_MUTACAO, randomize=True)
            self.POPULACAO.append(individuo)

    def reload(self):
        """
        Reload the current status of Generation and saves the best player if file
        """
        self._loaded = False
        self.BG_MAP.ObstacleBuilder.reset()
        self.seleciona_o_melhor()
        self.O_MELHOR.save_in_file()
        self.seleciona_populacao()
        self._loaded = True

    def restart(self):
        """
        Restarts the population if is empty, else will update the best player and the current player
        """
        self.stop()
        if len(self.POPULACAO) <= 0:
            self.reload()
        else:
            self.BG_MAP.ObstacleBuilder.reset()
            self.seleciona_o_melhor()
            self.atualiza_o_atual()
        self._loaded = True

    def start(self):
        """
        Starts IA Generation
        """
        self.seleciona_populacao_inicial()
        self._loaded = True

    def stop(self):
        """
        Stops the current Generation
        """
        self._loaded = False
