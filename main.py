import os
import pickle
from tqdm import tqdm
from my_parser import Parser
import configs as c
from preprocess_document import Preprocessor
from spimi import Index

# p = Parser()
# p.run(c.STOP_DOWNLOAD_SIZE)

# pp = Preprocessor()
# asd = pp.get_terms('corpus/482818.txt')
# print(asd)

index = dict()
index_name_dict = dict()
list_dir = os.listdir(c.PATH_TO_CORPUS)
for doc in tqdm(list_dir, ascii=True, desc='create index'):
    doc_id = 0
    path_to_doc = f'{c.PATH_TO_CORPUS}{doc}'
    doc_terms = Preprocessor.get_terms(path_to_doc)
    Index.update_index(index, doc_terms, doc_id)

    index_name_dict[doc_id] = doc
    doc_id += 1

with open('index.pickle', 'wb') as f:
    pickle.dump(index, f)

with open('index_name_dict.pickle', 'wb') as f:
    pickle.dump(index_name_dict, f)

