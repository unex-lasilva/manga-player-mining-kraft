from json import load, dump
from pathlib import Path
from src.classes.config import Config

class JsonFile:

    """
    Classe responsável por simplificar operações de leitura e escrita em arquivos JSON,
    permitindo que tais ações possam ser realizadas da forma mais conveniente possível.
    """

    def __init__(self, filepath):
        self.path = Path(filepath)

    def load(self):
        """
        Lê o conteúdo presente neste arquivo Json e retorna os dados obtidos em formato "dict".
        Se o arquivo não existe, retorna "None".
        """
        if not self.path.exists():
            return None
        with open(self.path, 'r', encoding="utf-8") as file:
            return load(file)

    def save(self, content: dict):
        """
        Armazena o conteúdo informado neste arquivo Json.
        :param content: Conteúdo a ser salvo neste arquivo Json. Deve ser um "dict".
        """
        with open(self.path, 'w', encoding="utf-8") as file:
            dump(content, file, ensure_ascii=False, indent=4)

class MetricsJsonFile(JsonFile):

    """
    Uma especialização da classe "JsonFile", voltada para a manipulação do arquivo Json que armanena as métricas obtidas
    a partir da execução do algoritmo.
    """

    def __init__(self, filepath = Config.METRICS_PATH):
        super().__init__(filepath)

    def save(self, rules):
        results = {
            "min_confidence": Config.MIN_CONFIDENCE,
            "min_support": Config.MIN_SUPPORT,
            "min_rating": Config.MIN_RATING,
            "rules": rules
        }
        super().save(results)