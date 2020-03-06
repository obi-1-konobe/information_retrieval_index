import os
import pickle
from tqdm import tqdm
from my_parser import Parser
import configs as c
from preprocess import Preprocessing
from spimi import GetIndex

# p = Parser()
# p.run(c.STOP_DOWNLOAD_SIZE)

# asd = Preprocessing.get_terms('corpus/482818.txt')
# print(asd)
# dsa = Preprocessing.get_terms('corpus/482814.txt')
# print(dsa)
# pp.get_terms('corpus/482818.txt')
# pp.get_terms('corpus/482814.txt')
# print(asd)

idx = GetIndex()
# idx.save_block_index()
idx.combine_block_index()

