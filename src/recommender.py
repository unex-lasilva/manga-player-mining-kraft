from src.config import Config

class MovieRecommender:
    def __init__(self, movie_patterns):
        # Guarda os padrões descobertos
        self.patterns = movie_patterns

    def suggest_movies(self, user_history):
        # Sugere filmes baseado no que o usuário já gostou
        recommendations = {}

        # Para cada filme que o usuário gostou
        for movie in user_history:
            if movie in self.patterns:
                # Calcula um score de recomendação
                score = self.patterns[movie] / sum(self.patterns.values())
                recommendations[movie] = score

        # Retorna os TOP_N mais relevantes
        return sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:Config.TOP_N_HISTORY]