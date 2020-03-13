"""
модуль содержит функции реализующие построение обратного индекса корпуса документов
"""
import os
import pickle
from tqdm import tqdm
import configs as c
from preprocess import Preprocessing


class GetIndex:
    """
    класс содержит функции реализующие построение обратного индекса корпуса документов
    """

    def save_block_index(self):
        """
        разбиваем корпус на блоки и для каждого блока строим обратный индекс и сохраняем его на диск
        :return:
        """
        corpus_list = os.listdir(c.PATH_TO_CORPUS)
        # хэш с доп.информацией
        doc_id_doc_name_dict = dict()
        block = []
        block_size = 0
        for doc in tqdm(corpus_list, ascii=True, desc='block index'):
            doc_path = f'{c.PATH_TO_CORPUS}{doc}'
            doc_size = os.path.getsize(doc_path)
            # пока не превышен лимит по памяти, набираем в блок документы
            if block_size < c.MEMORY_SIZE:
                block.append(doc)
                block_size += doc_size
                continue
            # не теряем последний документ
            block.append(doc)
            # строим индекс для блока и сохраняем его на диск
            self.get_block_index(block, doc_id_doc_name_dict)
            # очищаем память
            block = []
            block_size = 0

        # сохраняем хэш с доп.информацией на диск
        with open(f'{c.INDEX_DIR}doc_id_doc_name_dict.pickle', 'wb') as f:
            pickle.dump(doc_id_doc_name_dict, f)

    def get_block_index(self, block, doc_id_doc_name_dict):
        """
        строим обратный индекс для блока документов и сохраняем его на диск,
        обновляем хэш с доп.информацией
        :param block: блок документов
        :param doc_id_doc_name_dict: хэш с доп.информацией
        :return:
        """
        block_index = dict()
        # определяем article_id документа
        if len(doc_id_doc_name_dict.keys()) == 0:
            doc_id = 0
        else:
            doc_id = max(doc_id_doc_name_dict.keys()) + 1
        for doc in block:
            doc_path = f'{c.PATH_TO_CORPUS}{doc}'
            # преобразуем документ в массив термов
            doc_terms = Preprocessing.get_terms(doc_path)
            # обновляем блочный индекс и строим хэш с частотами термов в документе
            doc_tf_dict = self.update_index(block_index, doc_terms, doc_id)
            # сопоставляем название документа и хэш с частотами термов
            temp_dict = dict()
            temp_dict[doc] = doc_tf_dict
            # обновляем хэш с доп.информацией
            doc_id_doc_name_dict[doc_id] = temp_dict

            doc_id += 1

        with open(f'{c.TEMP_DIR}index_{doc_id - 1}.pickle', 'wb') as f:
            pickle.dump(block_index, f)

    def combine_block_index(self):
        """
        объединяем все блочные индексы в один общий обратный индекс
        :return:
        """
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
        """
        обновляем блочный индекс и строим хэш с частотами термов в документе
        :param index: блочный индекс
        :param term_stream: массив термов документа
        :param doc_id: article_id документа
        :return: хэш с частотами термов в документе
        """
        tf_dict = dict()
        for term in term_stream:
            # если терма нет в индексе, вносим его
            if term not in index:
                index[term] = [doc_id]
                # частота терма в документе
                tf_dict[term] = 1
            # если терм в индексе есть, но в данном документе он встретился впервые
            elif doc_id not in index[term]:
                index[term] += [doc_id]
                tf_dict[term] = 1
            # если терм в индексе есть и в документе уже обрабатывался
            else:
                tf_dict[term] += 1

        return tf_dict
