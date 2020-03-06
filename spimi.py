import os
import pickle
import configs as c
from tqdm import tqdm
from preprocess import Preprocessing


class GetIndex:
    def __init__(self):
        pass

    def save_block_index(self):
        corpus_list = os.listdir(c.PATH_TO_CORPUS)
        doc_id_doc_name_dict = dict()
        block = []
        block_size = 0
        for doc in tqdm(corpus_list, ascii=True, desc='block index'):
            doc_path = f'{c.PATH_TO_CORPUS}{doc}'
            doc_size = os.path.getsize(doc_path)
            if block_size < c.MEMORY_SIZE:
                block.append(doc)
                block_size += doc_size
                continue
            block.append(doc)
            self.get_block_index(block, doc_id_doc_name_dict)
            block = []
            block_size = 0

        with open(f'{c.INDEX_DIR}doc_id_doc_name_dict.pickle', 'wb') as f:
            pickle.dump(doc_id_doc_name_dict, f)

    def get_block_index(self, block, doc_id_doc_name_dict):
        block_index = dict()
        if len(doc_id_doc_name_dict.keys()) == 0:
            doc_id = 0
        else:
            doc_id = max(doc_id_doc_name_dict.keys()) + 1
        for doc in block:
            doc_path = f'{c.PATH_TO_CORPUS}{doc}'
            doc_terms = Preprocessing.get_terms(doc_path)
            doc_tf_dict = self.update_index(block_index, doc_terms, doc_id)

            temp_dict = dict()
            temp_dict[doc] = doc_tf_dict
            doc_id_doc_name_dict[doc_id] = temp_dict

            doc_id += 1

        with open(f'{c.TEMP_DIR}index_{doc_id - 1}.pickle', 'wb') as f:
            pickle.dump(block_index, f)

    def combine_block_index(self):
        list_dir = os.listdir(c.TEMP_DIR)
        index_list = sorted(list_dir, key=lambda x: int(x.strip('.pickle')[5:]))
        full_index = dict()
        for file in tqdm(index_list, ascii=True, desc='full index'):
            with open(f'{c.TEMP_DIR}{file}', 'rb') as f:
                index = pickle.load(f)
            for term in index.keys():
                if term not in full_index:
                    full_index[term] = index[term]
                else:
                    full_index[term] += index[term]
        with open(f'{c.INDEX_DIR}full_index.pickle', 'wb') as f:
            pickle.dump(full_index, f)

    @staticmethod
    def update_index(index, term_stream, doc_id):
        tf_dict = dict()
        for term in term_stream:
            if term not in index:
                index[term] = [doc_id]
                tf_dict[term] = 1
            elif doc_id not in index[term]:
                index[term] += [doc_id]
                tf_dict[term] = 1
            else:
                tf_dict[term] += 1

        return tf_dict

