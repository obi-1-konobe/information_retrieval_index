"""
модуль содержит функции реализующие парсинг статей с сайта
"""
import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import configs as c


class Parser:
    """
    класс содержит функции реализующие парсинг статей с сайта
    """

    def run(self, stop_size):
        """
        парсим корпус документов
        :param stop_size: размер еорпуса в Мбайтах
        :return:
        """
        # переводим Мбайты в байты
        stop_size *= 1000000
        dir_size = 0
        # article_id статьи с которой начинаем парсить в порядке убывания
        article_id = c.START_ID
        dir_path = c.PATH_TO_CORPUS
        # визуализация прогресса
        pbar = tqdm(total=stop_size)
        while dir_size <= stop_size:
            article = self.get_article(article_id)
            if article:
                article_size = os.path.getsize(f'{dir_path}{article}')
                dir_size += article_size
                pbar.update(article_size)
            article_id -= 1
        pbar.close()

    @staticmethod
    def get_article(article_id):
        """
        проверяем наличие статьи по id, если статья есть, то сохраняем ее в txt-файле на диске
        :param article_id: id статьи
        :return: название сохраненного файла или False
        """
        # выгрузка документа
        req = requests.get('https://habr.com/ru/post/' + str(article_id) + '/')
        # парсинг документа
        soup = BeautifulSoup(req.text, 'html5lib')
        # если нет стать с таким article_id, то возвращаем False
        if not soup.find("span", {"class": "post__title-text"}):
            return False
        else:
            title = soup.find("span", {"class": "post__title-text"}).text
            text = soup.find("div", {"class": "post__text"}).text
            time = soup.find("span", {"class": "post__time"}).text

            file_name = f'{article_id}.txt'
            with open(f'corpus/{file_name}', 'w', encoding='utf-8') as f:
                f.write(f'ID: {article_id}\ntime: {time}\ntitle: {title}\ntext: {text}')

            return file_name
