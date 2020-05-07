"""
модуль содержит функции реализующие парсинг статей с сайта
"""
import json
from tqdm import tqdm
import configs as c


class Parser:
    """
    класс содержит функции реализующие парсинг json
    """

    def run(self):
        """
        парсим корпус документов
        :return:
        """
        article_id: int = 0
        dir_path: str = c.PATH_TO_CORPUS
        with open('corpus/News_Category_Dataset_v2.json', 'r') as f:
            data = f.readlines()

        # визуализация прогресса
        for line in tqdm(data, ascii=True, desc='parser'):
            json_line = json.loads(line)
            # сохраняем заголовок и краткое сожержанее
            with open(f'{dir_path}{article_id}.txt', 'w+') as f:
                f.write(json_line['headline'])
                f.write('\n')
                f.write(json_line['short_description'])
            article_id += 1
