from typing import Dict

import json as JSON
import game.model.file as _FILE

from ..model.player import Player
from ..model.layer import BackgroundMap


class Individuo(Player):

    def __init__(self,
                 background: BackgroundMap,
                 cromossomo: Dict = None,
                 numero: int = -1, geracao: int = -1,
                 ):
        super().__init__(background=background)
        self.numero: int = numero
        self.geracao: int = geracao
        self.cromossomo: Dict = cromossomo

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
