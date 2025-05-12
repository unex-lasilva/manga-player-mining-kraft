import pandas as pd
from src.classes.config import Config

class DataProcessor:
    def __init__(self):
        # Pega as configurações do projeto
        self.config = Config

    def prepare_data(self):
        """Transforma dados brutos em formato útil para análise"""
        # Lê os arquivos CSV
        ratings = pd.read_csv(self.config.DATA_PATHS['ratings'])
        movies = pd.read_csv(self.config.DATA_PATHS['movies'], low_memory=False)

        # Limpa IDs inválidos dos filmes
        movies = movies[movies['id'].apply(lambda x: str(x).isdigit())]
        movies['id'] = movies['id'].astype(int)

        # Junta os dados num único DataFrame
        merged = ratings.merge(movies, left_on='movieId', right_on='id')

        # Filtra só avaliações positivas
        liked_movies = merged[merged['rating'] > self.config.MIN_RATING]

        # Agrupa filmes por usuário
        return liked_movies.groupby('userId')['title'].apply(list).to_dict()