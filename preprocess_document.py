from string import punctuation
import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem


class Preprocessor:
    def __init__(self):
        pass

    @staticmethod
    def get_terms(doc_name):
        # nltk.download('stopwords')
        ru_stopwords = stopwords.words('russian')
        mystem = Mystem()
        terms = []

        with open(doc_name, 'r', encoding='utf-8') as f:
            doc = f.readlines()

        for line in doc:
            tokens = mystem.lemmatize(line.lower())
            line_terms = [token for token in tokens \
                          if token not in ru_stopwords \
                          and token != ' ' \
                          and token.strip() not in punctuation]
            terms += line_terms

        return terms

