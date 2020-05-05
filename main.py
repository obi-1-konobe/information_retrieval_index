"""
интерфейсный модуль для оркестрации процессами программы.
"""
import pickle
from typing import Dict, List, Union

import configs as c
from my_parser import Parser
from preprocess import Preprocessing as pp
from spimi import GetIndex
from rank import RankList
from boolean_search import BooleanSearch as bs

# триггер на запуск парсера
if c.CORPUS_PARSER:
    p = Parser()
    p.run(c.STOP_DOWNLOAD_SIZE)
# триггер на сборку обратного индекса
if c.BUILD_INDEX:

    idx = GetIndex()
    idx.save_block_index()
    idx.combine_block_index()
# читаем с диска индекс и хэш с доп.информацией
with open('index/full_index.pickle', 'rb') as f:
    index: Dict[int, List] = pickle.load(f)
with open('index/doc_id_doc_name_dict.pickle', 'rb') as f:
    doc_id_doc_name_dict: Dict = pickle.load(f)

while True:
    print('\n\nInput your boolean query:')
    query_string: str = input('>')
    query_list: List[str] = query_string.split()
    # преобразуем в список массивов article_id и операций над ними
    arrays_and_operators, term_list = pp.process_query(
        query_list,
        index,
        doc_id_doc_name_dict
    )
    # считываем первый массив
    result: Union[str, List] = arrays_and_operators.pop(0)
    # пока в списке есть элементы
    while len(arrays_and_operators) > 0:
        operator: str = arrays_and_operators.pop(0)
        array: List[int] = arrays_and_operators.pop(0)

        if operator == 'AND':
            result: List[int] = bs.intersect(result, array)
        elif operator == 'OR':
            result: List[int] = bs.union(result, array)

    # ранжируем результаты поиска
    ranked_list, qty = RankList.rank_result_list(
        result,
        term_list,
        doc_id_doc_name_dict
    )
    print(f'{qty} results found')
    # вывод результатов на экран
    for doc_tuple in ranked_list:
        doc_name: str = doc_tuple[0]
        print_string: str = c.SEPARATOR
        with open(f'{c.PATH_TO_CORPUS}{doc_name}', 'r', encoding='utf-8') as f:
            for _ in range(3):
                print_string += f.readline()
        print(print_string)
