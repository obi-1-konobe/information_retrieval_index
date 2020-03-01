import os
import pickle
import configs as c

from preprocess_document import Preprocessor


class Index:
    def __init__(self):
        pass

    def get_block_index(self, doc_id_doc_name_dict, corpus_list, corpus_len):
        index = dict()
        doc_id = max(doc_id_doc_name_dict.keys()) + 1
        block_size = 0
        while block_size < c.MEMORY_SIZE and doc_id < corpus_len - 1:
            doc = corpus_list[doc_id]
            doc_path = f'{c.PATH_TO_CORPUS}{doc}'
            doc_terms = Preprocessor.get_terms(doc_path)
            self.update_index(index, doc_terms, doc_id)
            doc_size = os.path.getsize(doc_path)

            doc_id_doc_name_dict[doc_id] = doc
            block_size += doc_size
            doc_id += 1

        with open(f'{c.INDEX_DIR}index_{doc_id - 1}.pickle', 'wb') as f:
            pickle.dump(index, f)

    @staticmethod
    def update_index(index, term_stream, doc_id):
        for term in term_stream:
            if term not in index:
                some_dict = dict()
                some_dict[doc_id] = 1
                index[term] = some_dict
            else:
                index[term][doc_id] += 1



