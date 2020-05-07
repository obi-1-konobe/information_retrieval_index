"""
модуль содержит функции реализующие ранжирование документов
"""
import math
import numpy as np
import pandas as pd
import torch
import transformers as ppb
from typing import List, Dict, Tuple
from sklearn.metrics.pairwise import cosine_similarity

import configs as c


model_class, tokenizer_class, pretrained_weights = (
    ppb.DistilBertModel,
    ppb.DistilBertTokenizer,
    'distilbert-base-uncased'
)
tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
model = model_class.from_pretrained(pretrained_weights)


class RankList:
    """
    класс содержит функции реализующие ранжирование документов
    """

    def rank_list(
            self, result_list, term_list, doc_dict, query_string
    ) -> Tuple[List, int]:
        """
        ранжируем итоговую выдачу
        :param result_list: список результатов поиска
        :param term_list: список термов запроса
        :param doc_dict: хэш с доп.информацией
        :param query_string: строка запроса
        :return: топ10 отранжированных результатов
        и общее количество результатов
        """
        # получаем топ100 результатов по TF
        top_list, results_qty = self.get_top_results(
            result_list,
            term_list,
            doc_dict
        )
        # собираем данные для датафреима
        data: List[List] = [['query', query_string]]
        for doc_tuple in top_list:
            doc_name: str = doc_tuple[0]
            doc_path: str = f'{c.PATH_TO_CORPUS}{doc_name}'
            with open(doc_path, 'r') as f:
                text: str = f.read()
            data.append([doc_name, text])
        df = pd.DataFrame(data, columns=['file', 'text'])
        # токенизация
        tokenized = df['text'].apply(
            lambda x: tokenizer.encode(x, add_special_tokens=True)
        )
        # выравнивание длин массивов
        padded = self.zero_padding(tokenized)
        # пропускаем данные через BERT
        input_ids = torch.tensor(np.array(padded))
        with torch.no_grad():
            last_hidden_states = model(input_ids)
        # получаем эмбединги текстов
        features = last_hidden_states[0][:, 0, :].numpy()
        # считаем косинусную близость документов и запроса
        qty: int = len(features - 1)
        cos_similarity = cosine_similarity([features[0]], features[1:])[0]
        # ранжируем и выдаем топ10
        ordered_idx: List[int] = cos_similarity.argsort()[-qty:][::-1]
        result: List[str] = [df.file[i + 1] for i in ordered_idx if i < 10]
        return result, results_qty

    @staticmethod
    def zero_padding(tokenized_array):
        """
        выравнивание массивов нулями
        :param tokenized_array: массив токенов
        :return: выравненный массив
        """
        max_len = 0
        for i in tokenized_array.values:
            if len(i) > max_len:
                max_len = len(i)

        padded_array = np.array(
            [i + [0] * (max_len - len(i)) for i in tokenized_array.values]
        )
        return padded_array

    @staticmethod
    def get_top_results(
            result_list: List[int], term_list: List[str], doc_dict: Dict
    ) -> Tuple[List, int]:
        """
        ранжируем список результатов поиска по TF
        :param result_list: список результатов поиска
        :param term_list: список термов запроса
        :param doc_dict: хэш с доп.информацией
        :return: топ100 отранжированных результатов
        """
        temp_list: List[Tuple] = list()
        for doc_id in result_list:
            # получаем название документа
            doc_name: str = list(doc_dict[doc_id].keys())[0]
            # сумма term frequency
            sum_tf: float = 0
            for term in term_list:
                # проверяем наличие терма в хэше
                if term in doc_dict[doc_id][doc_name].keys():
                    # получаем term frequency терма в документе
                    tf: int = doc_dict[doc_id][doc_name][term]
                    sum_tf += math.log(tf)
            # записываем название документа и его term frequency в кортеж
            temp_list.append((doc_name, sum_tf))
        # сортируем по term frequency
        ranked_list: List[Tuple] = sorted(
            temp_list,
            key=lambda x: x[1],
            reverse=True
        )

        results_qty: int = len(ranked_list)
        if results_qty > 100:
            top_100: List[Tuple] = ranked_list[:100]
            return top_100, results_qty
        return ranked_list, results_qty
