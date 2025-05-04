import os
from pathlib import Path

class Config:
    # Obtém o caminho absoluto da pasta do projeto
    BASE_DIR = Path(__file__).parent.parent

    # Paths dos arquivos
    DATA_PATHS = {
        'ratings': os.path.join(BASE_DIR, 'data', 'ratings_small.csv'),
        'movies': os.path.join(BASE_DIR, 'data', 'movies_metadata.csv')
    }

    # Parâmetros do Apriori

    # Nota mínima para considerar que o usuário gostou
    MIN_RATING: float = 3.0

    # Configurações do algoritmo Apriori
    MIN_SUPPORT: float = 0.1 # Frequência mínima para ser considerado relevante
    MIN_CONFIDENCE: float = 0.7 # Chance mínima para fazer recomendação

    # Quantidade de recomendações
    TOP_N_HISTORY: int = 5 # Baseado no histórico completo
    TOP_N_LAST: int = 3 # Baseado no último filme assistido

