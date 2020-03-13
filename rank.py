"""
модуль содержит функции реализующие ранжирование документов
"""
import math
from typing import List, Dict, Tuple


class RankList:
    """
    класс содержит функции реализующие ранжирование документов
    """
    @staticmethod
    def rank_result_list(
            result_list: List[int],
            term_list: List[str],
            doc_dict: Dict
    ) -> Tuple[List, int]:
        """
        ранжируем список результатов поиска
        :param result_list: список результатов поиска
        :param term_list: список термов запроса
        :param doc_dict: хэш с доп.информацией
        :return: топ10 отранжированных результатов
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
        if results_qty > 10:
            top_10: List[Tuple] = ranked_list[:10]
            return top_10, results_qty
        return ranked_list, results_qty
