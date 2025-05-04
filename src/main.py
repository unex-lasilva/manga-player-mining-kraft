from data_processing import DataProcessor
from apriori import AprioriAnalyzer
from recommender import MovieRecommender

def main():
    print("🪄 Iniciando sistema de recomendação...")

    # 1. Pré-processa os dados
    print("Limpando e organizando dados...")
    data_processor = DataProcessor()
    user_movies = data_processor.prepare_data()

    # 2. Analisa padrões
    print("Procurando padrões nos dados...")
    apriori = AprioriAnalyzer()
    movie_patterns = apriori.find_patterns(user_movies)
    rules = apriori.generate_rules(movie_patterns, list(user_movies.values()))

    # 3. Prepara recomendações
    print("Preparando recomendações...")
    recommender = MovieRecommender(rules)

    # 4. Faz a recomendação de filmes
    user_history = user_movies[2]
    recommendations = recommender.recommend_from_history(user_history)
    print(user_history)
    print(recommendations)

if __name__ == "__main__":
    main()