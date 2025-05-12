from classes.apriori_analyzer import AprioriAnalyzer
from classes.data_processor import DataProcessor
from classes.config import Config
from classes.json_file import MetricsJsonFile
from classes.movie_recommender import MovieRecommender

def get_previous_metrics():
    metrics_json_file = MetricsJsonFile()
    if not metrics_json_file.path.exists():
        return

    metrics = metrics_json_file.load()
    metrics_saved_preset = [
        metrics["min_confidence"],
        metrics["min_support"],
        metrics["min_rating"]
    ]
    actual_preset = [ Config.MIN_CONFIDENCE, Config.MIN_SUPPORT, Config.MIN_RATING]
    if metrics_saved_preset != actual_preset:
        print("Regras armazenadas estão desatualizadas! Gerando novas...")
        return None

    return metrics['rules']

def main():
    print("🪄 Iniciando sistema de recomendação...")

    rules = get_previous_metrics()

    # 1. Pré-processa os dados
    print("Limpando e organizando dados...")
    data_processor = DataProcessor()
    user_movies = data_processor.prepare_data()

    if rules is None:

        # 2. Analisa padrões
        print("Procurando padrões nos dados...")
        apriori = AprioriAnalyzer()
        movie_patterns = apriori.find_patterns(user_movies)
        rules = apriori.generate_rules(movie_patterns, list(user_movies.values()))

        # 3. Armazena em um arquivo Json as regras obtidas com a execução do algoritmo
        print(f"Salvando as {len(rules)} regras obtidas...")
        MetricsJsonFile().save(rules)

    # 3. Prepara recomendações
    print("Preparando recomendações...")
    recommender = MovieRecommender(rules)

    # 4. Faz a recomendação de filmes
    print('-' * 80)
    print('-' * 35 + "RESULTADOS" + '-' * 35)
    print(f'Nível mínimo de suporte: {int(Config.MIN_SUPPORT * 100)} %')
    print(f'Nível mínimo de confiabilidade: {int(Config.MIN_CONFIDENCE * 100)} %')
    print('-' * 80)

    for userid, user_history in user_movies.items():
        if userid == 10: break
        user_last_watched_movie = user_history[-1]
        recommendations_by_history = recommender.recommend_from_history(user_history)
        recommendations_by_last_movie = recommender.recommend_from_last_movie(user_last_watched_movie, user_history)
        print('Histórico de filmes assistidos:', user_history)
        print('Último filme que gostou:', user_last_watched_movie)
        print('Recomendação com base no histórico:', recommendations_by_history)
        print('Recomendação com base no último filme:', recommendations_by_last_movie)
        print('-' * 80)

if __name__ == "__main__":
    main()