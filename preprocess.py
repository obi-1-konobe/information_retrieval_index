"""
модуль содержит функции реализующие обработку документов в термы
"""
import nltk
from typing import List, Dict, Union, Tuple
import configs as c
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from boolean_search import BooleanSearch as bs
# инициализация лексических библиотек
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


class Preprocessing:
    """
    класс содержит функции реализующие обработку документов в термы
    """
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')

    @staticmethod
    def get_terms(doc_path: str) -> List[str]:
        """
        преобразуем документ в массив термов
        :param doc_path: путь к документу
        :return: массив термов
        """

        en_stopwords = stopwords.words('english')
        lemmatizer = WordNetLemmatizer()
        with open(doc_path, 'r', encoding='utf-8') as f:
            doc: List[str] = f.readlines()

        terms: List[str] = []
        for line in doc:
            # сплитим строку по небуквенным символам
            tokens: List[str] = nltk.word_tokenize(line)
            filtered_tokens = [w for w in tokens if w not in en_stopwords]
            # приводим слова к номальной форме
            terms += [lemmatizer.lemmatize(token) for token in filtered_tokens]

        return terms

    @staticmethod
    def process_query(
            query_list: List[str],
            index: Dict[int, List],
            doc_id_dict: Dict
    ) -> Tuple[List, List]:
        """
        преобразовываем запрос в последовательность массивов article_id
        документов и операций над ними
        :param query_list: список термов и операций
        :param index: обратный индекс корпуса документов
        :param doc_id_dict: хэш с доп.информацией
        :return: список массивов и операций, список термов
        """
        temp_list: List[str] = list()
        lemmatizer = WordNetLemmatizer()
        for token in query_list:
            # преобразуем слова, операторы не изменяем
            if token not in c.OPERATORS:
                temp_list.append(lemmatizer.lemmatize(token))
            else:
                temp_list.append(token)

        # в term_list будем хранить термы из запроса
        term_list: List[str] = list()
        result_list: List[Union[str, List]] = list()
        while len(temp_list) > 0:
            query_part: str = temp_list.pop(0)
            if query_part == 'NOT':
                next_part: str = temp_list.pop(0)
                result: List[int] = bs.not_query(next_part, index, doc_id_dict)
            elif query_part == 'AND' or query_part == 'OR':
                result_list.append(query_part)
                continue
            elif query_part in index.keys():
                result: List[int] = index[query_part]
                term_list.append(query_part)
            else:
                result: List[int] = list()
            result_list.append(result)

        return result_list, term_list
