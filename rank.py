import math


class RankList:
    @staticmethod
    def rank_result_list(result_list, term_list, doc_dict):
        """
        ранжируем список результатов поиска
        :param result_list: список результатов поиска
        :param term_list: список термов запроса
        :param doc_dict: хэш с доп.информацией
        :return: топ10 отранжированных результатов
        """
        temp_list = []
        for doc_id in result_list:
            # получаем название документа
            doc_name = list(doc_dict[doc_id].keys())[0]
            # сумма term frequency
            sum_tf = 0
            for term in term_list:
                # проверяем наличие терма в хэше
                if term in doc_dict[doc_id][doc_name].keys():
                    # получаем term frequency терма в документе
                    tf = doc_dict[doc_id][doc_name][term]
                    sum_tf += math.log(tf)
            # записываем название документа и его term frequency в кортеж
            temp_list.append((doc_name, sum_tf))
        # сортируем по term frequency
        ranked_list = sorted(temp_list, key=lambda x: x[1], reverse=True)

        if len(ranked_list) > 10:
            top_10 = ranked_list[:10]
            return top_10
        return ranked_list
