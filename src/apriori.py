from src.config import Config
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
                support = calc_support(*itemset, items_lists=transactions)
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

                    confidence = calc_confidence(antecedent, consequent, items_lists=transactions)

                    if confidence >= self.config.MIN_CONFIDENCE:
                        lift = calc_lift(antecedent, consequent, items_lists=transactions)
                        rules.append({
                            'antecedent': antecedent,
                            'consequent': consequent,
                            'confidence': confidence,
                            'lift': lift
                        })

        return rules

def get_itemset(items_lists):
    """
    Função para obter o itemset a partir de uma listagem de dados
    :param items_lists: note que "lists" está no plural, logo, espera-se uma lista de listas aqui
    :return: um conjunto unificado dos dados presentes na listagem recebida, sem repetições
    """
    itemset = set()
    for items_list in items_lists:
        itemset = itemset.union(set(items_list))
    return itemset

def calc_frequency(*item_or_items, items_lists):
    """
    Função para descobrir em quantos registros dentro de "items_list", um item ou vários itens aparecem juntos
    :param item_or_items: item(s) que se deseja descobrir o número de aparições em conjunto dentro de cada registro em "items_list"
    :param items_lists: note que "lists" está no plural, logo, espera-se uma lista de listas aqui
    :return: um número inteiro representando o número de registros dentro de "item_lists" em que os itens passados estão presentes
    """
    frequency = 0
    for items_list in items_lists:
        all_items_was_found = True
        for item in item_or_items:
            if item not in items_list:
                all_items_was_found = False
        if all_items_was_found:
            frequency += 1
    return frequency

def calc_support(*item_or_items, items_lists):
    """
    Função para calcular e obter o suporte para um ou vários itens. Se vários itens forem passados, calculará o suporte
    buscando registros em que todos os ítens passados estejam presentes ao mesmo tempo.
    :param item_or_items: item ou uma junção (lista) de itens
    :param items_lists: note que "lists" está no plural, logo, espera-se uma lista de listas aqui
    :return: um número real representando o nível do suporte que um item ou a junção dos itens passados possuem
    """
    registries_number = len(items_lists)
    item_frequency = calc_frequency(*item_or_items, items_lists=items_lists)
    return item_frequency / registries_number

def calc_confidence(antecedents, consequents, items_lists):
    """
    Função para calcular e obter o nível de confiança, considerando os antecedentes e consequentes passados.
    Use a seguinte fórmula como base:
    * Confiança(antecedentes -> consequentes) = suporte(antecedentes U consequentes) / suporte(antecedentes)
    :param antecedents: lista contendo os dados antecedentes (dados que levam aos consequentes)
    :param consequents: lista contendo os dados consequentes (dados resultados da ocorrência dos antecedentes)
    :param items_lists: note que "lists" está no plural, logo, espera-se uma lista de listas aqui
    :return: um número real representando o nível da confiança, considerando os antecedentes e consequentes passados.
    """
    all_elements = antecedents + consequents
    full_support = calc_support(*all_elements, items_lists=items_lists)
    antecedents_support = calc_support(*antecedents, items_lists=items_lists)
    return full_support / antecedents_support

def calc_lift(antecedents, consequents, items_lists):
    """
    Função para calcular e obter o nível de correlação entre os antecedentes e consequentes passados.
    Use a seguinte fórmula como base:
    * Lift(antecedentes -> consequentes) = suporte(antecedentes U consequentes) / suporte(antecedentes) * suporte(antecedentes)
    :param antecedents: lista contendo os dados antecedentes (dados que, em tese, levam aos consequentes)
    :param consequents: lista contendo os dados consequentes (dados que, em tese, seriam resultados da ocorrência dos antecedentes)
    :param items_lists: note que "lists" está no plural, logo, espera-se uma lista de listas aqui
    :return: um número real representando o nível da correlação obtida a partir dos antecedentes e consequentes passados.
    """
    all_elements = antecedents + consequents
    full_support = calc_support(*all_elements, items_lists=items_lists)
    antecedents_support = calc_support(*antecedents, items_lists=items_lists)
    consequents_support = calc_support(*consequents, items_lists=items_lists)
    return full_support / (antecedents_support * consequents_support)