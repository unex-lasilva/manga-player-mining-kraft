import os
from pathlib import Path

class Config:
    # Obtém o caminho absoluto da pasta do projeto
    BASE_DIR = Path(__file__).parent.parent.parent

    # Obtém o caminho absoluto do local aonde as métricas obtidas são armazenadas
    METRICS_PATH = BASE_DIR / 'metrics.json'

    # Obtém o caminho absoluto da pasta contendo os bancos de dados utilizados pelo algoritmo
    DATA_DIR = BASE_DIR / 'data'

    # Paths dos arquivos
    DATA_PATHS = {
        'ratings': DATA_DIR / 'ratings_small.csv',
        'movies': DATA_DIR / 'movies_metadata.csv',
    }

    # Parâmetros do Apriori

    # Nota mínima para considerar que o usuário gostou
    MIN_RATING: float = 3.0

    # Configurações do algoritmo Apriori
    MIN_SUPPORT: float = 0.05  # Frequência mínima para ser considerado relevante
    MIN_CONFIDENCE: float = 0.6  # Chance mínima para fazer recomendação

    # Quantidade de recomendações
    TOP_N_HISTORY: int = 5  # Baseado no histórico completo
    TOP_N_LAST: int = 3  # Baseado no último filme assistido