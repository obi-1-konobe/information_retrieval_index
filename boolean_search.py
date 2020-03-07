class BooleanSearch:
    # def __init__(self, index):
    #     self.index = index
    @staticmethod
    def intersect(list_1, list_2):
        result_list = []
        iter_1 = iter(list_1)
        iter_2 = iter(list_2)
        length_1 = len(list_1)
        length_2 = len(list_2)

        if length_1 > length_2:
            max_value = list_2[-1]
        else:
            max_value = list_1[-1]

        doc_1 = next(iter_1)
        doc_2 = next(iter_2)
        while doc_1 < max_value and doc_2 < max_value:
            if doc_1 == doc_2:
                result_list.append(doc_1)
                doc_1 = next(iter_1)
                doc_2 = next(iter_2)
            else:
                if doc_1 < doc_2:
                    doc_1 = next(iter_1)
                else:
                    doc_2 = next(iter_2)

        if doc_1 == doc_2:
            result_list.append(doc_1)

        return result_list

    @staticmethod
    def union(list_1, list_2):
        result_list = []
        length_1 = len(list_1)
        length_2 = len(list_2)

        if length_1 > length_2:
            max_idx = length_2 - 1
        else:
            max_idx = length_1 - 1

        idx_1 = 0
        idx_2 = 0
        while idx_1 <= max_idx and idx_2 <= max_idx:
            doc_1 = list_1[idx_1]
            doc_2 = list_2[idx_2]
            if doc_1 > doc_2:
                result_list.append(doc_2)
                idx_2 += 1
            elif doc_1 < doc_2:
                result_list.append(doc_1)
                idx_1 += 1
            else:
                result_list.append(doc_1)
                idx_1 += 1
                idx_2 += 1

        result_list += list_1[idx_1:]
        result_list += list_2[idx_2:]

        return result_list

    @staticmethod
    def query_not_query(list_1, list_2):
        result_list = []
        length_1 = len(list_1)
        length_2 = len(list_2)

        if length_1 > length_2:
            max_idx = length_2 - 1
        else:
            max_idx = length_1 - 1

        idx_1 = 0
        idx_2 = 0
        while idx_1 <= max_idx and idx_2 <= max_idx:
            doc_1 = list_1[idx_1]
            doc_2 = list_2[idx_2]
            if doc_1 > doc_2:
                result_list.append(doc_2)
                idx_2 += 1
            elif doc_1 < doc_2:
                result_list.append(doc_1)
                idx_1 += 1
            else:
                idx_1 += 1
                idx_2 += 1

        result_list += list_1[max_idx + 1:]

        return result_list

