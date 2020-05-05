"""
модуль содержит функции реализующие парсинг статей с сайта
"""
import os
import json
import requests
from typing import Union
from bs4 import BeautifulSoup
from tqdm import tqdm
import configs as c


class Parser:
    """
    класс содержит функции реализующие парсинг статей с сайта
    """

    def run(self, stop_size: int):
        """
        парсим корпус документов
        :param stop_size: размер еорпуса в Мбайтах
        :return:
        """
        # переводим Мбайты в байты
        article_id: int = 0
        dir_path: str = c.PATH_TO_CORPUS
        with open('corpus/News_Category_Dataset_v2.json', 'r') as f:
            data = f.readlines()

        # визуализация прогресса
        for line in tqdm(data, ascii=True, desc='parser'):
            json_line = json.loads(line)
            with open(f'{dir_path}{article_id}.txt', 'w+') as f:
                f.write(json_line['headline'])
                f.write('\n')
                f.write(json_line['short_description'])
            article_id += 1

