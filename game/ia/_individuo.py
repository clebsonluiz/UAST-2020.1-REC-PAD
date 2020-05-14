from typing import Dict

import json as JSON
import game.model.file as _FILE

from ..model.player import Player
from ..model.layer import BackgroundMap
from ._rede_neural import RedeNeural


class Individuo(Player):

    def __init__(self,
                 background: BackgroundMap,
                 cromossomo: Dict = None,
                 numero: int = -1, geracao: int = -1,
                 ):
        super().__init__(background=background)
        self.background: BackgroundMap = background
        self.numero: int = numero
        self.geracao: int = geracao
        self.cromossomo: Dict = cromossomo
        self.cerebro: RedeNeural = RedeNeural(individuo=self)

    def create_cromossomo(self, randomize: bool = False):
        var: Dict = {
            'GN01': 0, 'GN02': 0,
            'GN11': 0, 'GN12': 0,
            'GN21': 0, 'GN22': 0,
            'GN31': 0, 'GN32': 0,
            'GN41': 0, 'GN42': 0,

            'GF01': 0, 'GF11': 0,
            'GF02': 0, 'GF12': 0,
            'GF21': 0, 'GF22': 0,
        }

        if randomize:
            from random import random as r, randint
            for k in var:
                var[k] = int(r() * (-1 if(randint(0, 1)) else 1))

        if self.cromossomo is None or len(self.cromossomo) == 0:
            self.cromossomo = var
            return self.cromossomo
        return var

    def update(self):
        super().update()
        self.cerebro.update()

    def clone(self) -> 'Individuo':
        return Individuo(self.background,
                         cromossomo=self.cromossomo.copy(),
                         numero=self.numero,
                         geracao=self.geracao)

    def to_json(self) -> Dict:
        return {
            'numero': self.numero,
            'geracao': self.geracao,
            'cromossomo': self.cromossomo
        }

    def save_in_file(self):
        _FILE.write(JSON.dumps(self.to_json()))
        _FILE.close_all()

    @staticmethod
    def load_from_file(background: BackgroundMap):
        file_json = _FILE.read()
        _FILE.close_all()

        if file_json is None or len(file_json) <= 0:
            file_json = "{}"

        return Individuo.from_json(file_json, background)

    @staticmethod
    def from_json(json, background: BackgroundMap):

        var = JSON.loads(json)
        numero = var.get('numero')
        geracao = var.get('geracao')
        cromossomo = var.get('cromossomo')
        return Individuo(background=background,
                         numero=numero if (numero is not None) else -1,
                         geracao=geracao if (geracao is not None) else -1,
                         cromossomo=cromossomo)

    # @staticmethod
    # def random(interval: tuple):
    #     var = interval
    #     return r() if var is None or len(var) < 2 else randint(var[0], var[1])
