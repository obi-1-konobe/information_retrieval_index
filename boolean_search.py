import configs as c


class BooleanSearch:

    @staticmethod
    def intersect(list_1, list_2):
        """
        пересечение массивов
        :param list_1: массив id документов первого аргумента
        :param list_2: массив id документов второго аргумента
        :return: результирующий массив
        """
        result_list = []
        if len(list_1) == 0 or len(list_2) == 0:
            return result_list
        # инициализируем итераторы
        iter_1 = iter(list_1)
        iter_2 = iter(list_2)

        # пока не закончится самый короткий массив
        doc_1 = next(iter_1)
        doc_2 = next(iter_2)
        while True:
            try:
                if doc_1 == doc_2:
                    result_list.append(doc_1)
                    doc_1 = next(iter_1)
                    doc_2 = next(iter_2)
                else:
                    if doc_1 < doc_2:
                        doc_1 = next(iter_1)
                    else:
                        doc_2 = next(iter_2)
            except StopIteration:
                break

        return result_list

    @staticmethod
    def union(list_1, list_2):
        """
        объединение массивов
        :param list_1: массив id документов первого аргумента
        :param list_2: массив id документов второго аргумента
        :return: результирующий массив
        """
        result_list = []
        # определяем  индекс последнего элемента в самом коротком массиве
        max_idx_1 = len(list_1) - 1
        max_idx_2 = len(list_2) - 1

        idx_1 = 0
        idx_2 = 0
        # пока не закончится самый короткий массив
        while idx_1 <= max_idx_1 and idx_2 <= max_idx_2:
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
        # добаляем остатки длинного массива
        result_list += list_1[idx_1:]
        result_list += list_2[idx_2:]

        return result_list

    @staticmethod
    def not_query(query, index, doc_id_dict):
        """
        отрицание
        :param query: терм
        :param index: обратный индекс корпуса документов
        :param doc_id_dict: хэш с доп.информацией
        :return: результирующий массив
        """
        doc_id_list = list(doc_id_dict.keys())
        if query not in index.keys():
            return doc_id_list
        list_1 = index[query]
        result_list = []
        # определяем  индекс последнего элемента в массиве
        max_idx = len(list_1) - 1

        idx_1 = 0
        idx_2 = 0
        # пока не закончится самый короткий массив
        while idx_1 <= max_idx:
            doc_1 = list_1[idx_1]
            doc_2 = doc_id_list[idx_2]
            if doc_1 > doc_2:
                result_list.append(doc_2)
                idx_2 += 1
            else:
                idx_1 += 1
                idx_2 += 1
        # добавляем остатки первого массива
        result_list += doc_id_list[idx_2:]

        return result_list

