import pymorphy2
import nltk
import re
import configs as c
from nltk.corpus import stopwords
from boolean_search import BooleanSearch as bs
# инициализация лексических библиотек
morph = pymorphy2.MorphAnalyzer()
nltk.download('stopwords')
ru_stopwords = stopwords.words('russian')


class Preprocessing:

    @staticmethod
    def get_terms(doc_path):
        """
        преобразуем документ в массив термов
        :param doc_path: путь к документу
        :return: массив термов
        """
        with open(doc_path, 'r', encoding='utf-8') as f:
            doc = f.readlines()

        terms = []
        for line in doc:
            # сплитим строку по небуквенным символам
            tokens = re.split('\W', line)
            # приводим слова к номальной форме
            terms += [morph.parse(token)[0].normal_form for token in tokens \
                      if token != '' \
                      and token not in ru_stopwords]

        return terms

    @staticmethod
    def process_query(query_list, index, doc_id_dict):
        """
        получаем термы из строки запроса
        :param query_list: токенизированная строка запроса
        :return: термы запроса
        """
        temp_list = []
        for token in query_list:
            # преобразуем слова, операторы не изменяем
            if token not in c.OPERATORS:
                temp_list.append(morph.parse(token)[0].normal_form)
            else:
                temp_list.append(token)

        # в term_list будем хранить термы из запроса
        term_list = []
        result_list = []
        while len(temp_list) > 0:
            query_part = temp_list.pop(0)
            if query_part == 'NOT':
                next_part = temp_list.pop(0)
                result = bs.not_query(next_part, index, doc_id_dict)
            elif query_part == 'AND' or query_part == 'OR':
                result_list.append(query_part)
                continue
            elif query_part in index.keys():
                result = index[query_part]
                term_list.append(query_part)
            else:
                result = []
            result_list.append(result)

        return result_list, term_list
