class AprioriMetrics:

    @staticmethod
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

    @staticmethod
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

    @classmethod
    def calc_support(cls, *item_or_items, items_lists):
        """
        Função para calcular e obter o suporte para um ou vários itens. Se vários itens forem passados, calculará o suporte
        buscando registros em que todos os ítens passados estejam presentes ao mesmo tempo.
        :param item_or_items: item ou uma junção (lista) de itens
        :param items_lists: note que "lists" está no plural, logo, espera-se uma lista de listas aqui
        :return: um número real representando o nível do suporte que um item ou a junção dos itens passados possuem
        """
        registries_number = len(items_lists)
        item_frequency = cls.calc_frequency(*item_or_items, items_lists=items_lists)
        return item_frequency / registries_number

    @classmethod
    def calc_confidence(cls, antecedents, consequents, items_lists):
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
        full_support = cls.calc_support(*all_elements, items_lists=items_lists)
        antecedents_support = cls.calc_support(*antecedents, items_lists=items_lists)
        return full_support / antecedents_support

    @classmethod
    def calc_lift(cls, antecedents, consequents, items_lists):
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
        full_support = cls.calc_support(*all_elements, items_lists=items_lists)
        antecedents_support = cls.calc_support(*antecedents, items_lists=items_lists)
        consequents_support = cls.calc_support(*consequents, items_lists=items_lists)
        return full_support / (antecedents_support * consequents_support)