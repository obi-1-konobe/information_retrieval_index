import os
import pickle
from tqdm import tqdm
from my_parser import Parser
import configs as c
from preprocess import Preprocessing
from spimi import GetIndex
from rank import RankList
from boolean_search import BooleanSearch as bs

# p = Parser()
# p.run(c.STOP_DOWNLOAD_SIZE)

# asd = Preprocessing.get_terms('corpus/482818.txt')
# print(asd)
# dsa = Preprocessing.get_terms('corpus/482814.txt')
# print(dsa)
# pp.get_terms('corpus/482818.txt')
# pp.get_terms('corpus/482814.txt')
# print(asd)

# idx = GetIndex()
# idx.save_block_index()
# idx.combine_block_index()

with open('index/full_index.pickle', 'rb') as f:
    index = pickle.load(f)
with open('index/doc_id_doc_name_dict.pickle', 'rb') as f:
    doc_id_doc_name_dict = pickle.load(f)


while True:
    print('Input your boolean query:')
    query_string = input('>')
    query_list = query_string.split()
    query_list = Preprocessing.get_query_terms(query_list)
    query_1 = query_list.pop(0)
    if query_1 in index.keys():
        result = index[query_1]
    else:
        result = []
    term_list = [query_1]
    while len(query_list) > 0:
        operator = query_list.pop(0)
        query_2 = query_list.pop(0)
        if query_2 in index.keys():
            list_2 = index[query_2]
        else:
            list_2 = []
        if operator == 'AND':
            result = bs.intersect(result, list_2)
            term_list.append(query_2)
        elif operator == 'OR':
            result = bs.union(result, list_2)
            term_list.append(query_2)
        elif operator == 'NOT':
            result = bs.query_not_query(result, list_2)

    ranked_list = RankList.rank_result_list(result, term_list, doc_id_doc_name_dict)
    for doc_tuple in ranked_list:
        doc_name = doc_tuple[0]
        print_string = c.SEPARATOR
        with open(f'{c.PATH_TO_CORPUS}{doc_name}', 'r', encoding='utf-8') as f:
            for _ in range(3):
                print_string += f.readline()
        url = 'https://habr.com/ru/post/' + doc_name.strip('.txt') + '/'
        print_string += f'url: {url}'
        print(print_string)









