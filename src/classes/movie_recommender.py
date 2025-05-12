from src.classes.config import Config

class MovieRecommender:
    def __init__(self, association_rules):
        # Guarda as regras obtidas
        self.rules = association_rules

    def recommend_from_history(self, user_history, top_n=Config.TOP_N_HISTORY):
        recommendations = {}
        for rule in self.rules:
            if set(rule['antecedent']).issubset(set(user_history)):
                for movie in rule['consequent']:
                    if movie not in user_history:
                        recommendations[movie] = max(recommendations.get(movie, 0), rule['confidence'])
        # Ordenar as recomendações por confiança
        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return [movie for movie, _ in sorted_recommendations[:top_n]]

    def recommend_from_last_movie(self, last_movie, user_history, top_n=Config.TOP_N_LAST):
        recommendations = {}
        for rule in self.rules:
            if set(rule['antecedent']) == {last_movie} or last_movie in rule['antecedent']:
                for movie in rule['consequent']:
                    if movie not in user_history:
                        recommendations[movie] = max(recommendations.get(movie, 0), rule['confidence'])
        # Ordenar as recomendações por confiança
        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return [movie for movie, _ in sorted_recommendations[:top_n]]