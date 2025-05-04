from src.config import Config

class AprioriAnalyzer:

    def __init__(self):
        # Configurações do algoritmo
        self.config = Config

    def find_patterns(self, user_movies):
        # Descobre quais filmes aparecem juntos frequentemente
        # Conta quantas vezes cada filme aparece
        movie_counts = {}
        for movies in user_movies.values():
            for movie in set(movies):  # Remove duplicatas por usuário
                movie_counts[movie] = movie_counts.get(movie, 0) + 1

        # Filtra pelos filmes mais frequentes
        return {
            movie: count
            for movie, count in movie_counts.items()
            if count / len(user_movies) >= self.config.MIN_SUPPORT
        }
