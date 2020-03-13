"""
модуль содержит функции реализующие элементы математической логики
"""
from typing import List, Iterator, Dict


class BooleanSearch:
    """
    класс содержит функции реализующие элементы математической логики
    """

    @staticmethod
    def intersect(list_1: List[int], list_2: List[int]) -> List[int]:
        """
        пересечение массивов
        :param list_1: массив article_id документов первого аргумента
        :param list_2: массив article_id документов второго аргумента
        :return: результирующий массив
        """
        result_list: List[int] = list()
        if len(list_1) == 0 or len(list_2) == 0:
            return result_list
        # инициализируем итераторы
        iter_1: Iterator = iter(list_1)
        iter_2: Iterator = iter(list_2)

        # пока не закончится самый короткий массив
        doc_1: int
        doc_2: int
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
    def union(list_1: List[int], list_2: List[int]) -> List[int]:
        """
        объединение массивов
        :param list_1: массив article_id документов первого аргумента
        :param list_2: массив article_id документов второго аргумента
        :return: результирующий массив
        """
        result_list: List[int] = list()
        # определяем  индекс последнего элемента в самом коротком массиве
        max_idx_1: int = len(list_1) - 1
        max_idx_2: int = len(list_2) - 1

        idx_1: int = 0
        idx_2: int = 0
        # пока не закончится самый короткий массив
        while idx_1 <= max_idx_1 and idx_2 <= max_idx_2:
            doc_1: int = list_1[idx_1]
            doc_2: int = list_2[idx_2]
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
    def not_query(
            query: str,
            index: Dict[str, List[int]],
            doc_id_dict: Dict
    ) -> List[int]:
        """
        отрицание
        :param query: терм
        :param index: обратный индекс корпуса документов
        :param doc_id_dict: хэш с доп.информацией
        :return: результирующий массив
        """
        doc_id_list: List[int] = list(doc_id_dict.keys())
        if query not in index.keys():
            return doc_id_list
        list_1: List[int] = index[query]
        result_list: List[int] = list()
        # определяем  индекс последнего элемента в массиве
        max_idx: int = len(list_1) - 1

        idx_1: int = 0
        idx_2: int = 0
        # пока не закончится самый короткий массив
        while idx_1 <= max_idx:
            doc_1: int = list_1[idx_1]
            doc_2: int = doc_id_list[idx_2]
            if doc_1 > doc_2:
                result_list.append(doc_2)
                idx_2 += 1
            else:
                idx_1 += 1
                idx_2 += 1
        # добавляем остатки первого массива
        result_list += doc_id_list[idx_2:]

        return result_list
