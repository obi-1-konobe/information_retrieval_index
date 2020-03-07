import os
import pickle
from tqdm import tqdm
from my_parser import Parser
import configs as c
from preprocess import Preprocessing
from spimi import GetIndex
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

while True:
    print('Input your boolean query:')
    query_string = input('>')
    query_list = query_string.split()
    query_1 = query_list.pop(0)
    result = index[query_1]
    # query_2 = None
    # list_2 = None
    # operator = None
    while len(query_list) > 0:
        operator = query_list.pop(0)
        query_2 = query_list.pop(0)
        list_2 = index[query_2]
        if operator == 'AND':
            result = bs.intersect(result, list_2)
        elif operator == 'OR':
            result = bs.union(result, list_2)
        elif operator == 'NOT':
            result = bs.query_not_query(result, list_2)










