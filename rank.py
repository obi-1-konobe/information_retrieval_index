import math


class RankList:
    @staticmethod
    def rank_result_list(result_list, term_list, doc_dict):
        temp_list = []
        for doc_id in result_list:
            doc_name = list(doc_dict[doc_id].keys())[0]
            sum_tf = 0
            for term in term_list:
                if term in doc_dict[doc_id][doc_name].keys():
                    tf = doc_dict[doc_id][doc_name][term]
                    sum_tf += math.log(tf)
            temp_list.append((doc_name, sum_tf))

        ranked_list = sorted(temp_list, key=lambda x: x[1], reverse=True)

        if len(ranked_list) > 10:
            top_10 = ranked_list[:10]
            return top_10
        return ranked_list
