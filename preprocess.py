import pymorphy2
import nltk
import re
import configs as c
from nltk.corpus import stopwords

morph = pymorphy2.MorphAnalyzer()
nltk.download('stopwords')
ru_stopwords = stopwords.words('russian')


class Preprocessing:

    @staticmethod
    def get_terms(doc_path):
        with open(doc_path, 'r', encoding='utf-8') as f:
            doc = f.readlines()

        terms = []
        for line in doc:
            tokens = re.split('\W', line)
            terms += [morph.parse(token)[0].normal_form for token in tokens \
                      if token != '' \
                      and token not in ru_stopwords]

        return terms

    @staticmethod
    def get_query_terms(query_list):
        result_list = []
        for token in query_list:
            if token not in c.OPERATORS:
                result_list.append(morph.parse(token)[0].normal_form)
            else:
                result_list.append(token)

        return result_list


