from classes.apriori_metrics import AprioriMetrics
from classes.config import Config
from itertools import combinations

class AprioriAnalyzer:

    def __init__(self):
        # Configurações do algoritmo
        self.config = Config

    def find_patterns(self, user_movies):
        """
        Descobre itemsets frequentes a partir do histórico de usuários.
        :param user_movies: dict com userId como chave e lista de filmes como valor
        :return: lista de tuplas contendo os itemsets frequentes e seus suportes
        """
        transactions = list(user_movies.values())
        itemsets = []
        all_frequent_itemsets = []

        # Primeiro: itemsets de tamanho 1
        unique_items = set(item for movies in transactions for item in movies)
        current_itemsets = [{item} for item in unique_items]

        k = 1
        while current_itemsets:
            frequent_itemsets = []

            for itemset in current_itemsets:
                support = AprioriMetrics.calc_support(*itemset, items_lists=transactions)
                if support >= self.config.MIN_SUPPORT:
                    frequent_itemsets.append((itemset, support))

            # Salva os itemsets frequentes desse tamanho
            all_frequent_itemsets.extend(frequent_itemsets)

            # Gera combinações para próximo tamanho (k+1)
            next_items = [iset[0] for iset in frequent_itemsets]
            new_candidates = set()

            for i in range(len(next_items)):
                for j in range(i + 1, len(next_items)):
                    union = next_items[i].union(next_items[j])
                    if len(union) == k + 1:
                        new_candidates.add(frozenset(union))

            current_itemsets = list(new_candidates)
            k += 1

        return all_frequent_itemsets

    def generate_rules(self, frequent_itemsets, transactions):
        """
        Gera regras de associação a partir de itemsets frequentes.
        :param frequent_itemsets: lista de tuplas (itemset, suporte)
        :param transactions: lista de listas (filmes curtidos por cada usuário)
        :return: lista de regras no formato:
                 {'antecedent': [...], 'consequent': [...], 'confidence': x, 'lift': y}
        """
        rules = []

        for itemset, support in frequent_itemsets:
            if len(itemset) < 2:
                continue  # Não gera regras com item único

            items = list(itemset)
            for i in range(1, len(items)):
                antecedent_combinations = combinations(items, i)
                for antecedent in antecedent_combinations:
                    antecedent = list(antecedent)
                    consequent = list(set(items) - set(antecedent))

                    confidence = AprioriMetrics.calc_confidence(antecedent, consequent, items_lists=transactions)

                    if confidence >= self.config.MIN_CONFIDENCE:
                        lift = AprioriMetrics.calc_lift(antecedent, consequent, items_lists=transactions)
                        rules.append({
                            'antecedent': antecedent,
                            'consequent': consequent,
                            'confidence': confidence,
                            'lift': lift
                        })

        return rules