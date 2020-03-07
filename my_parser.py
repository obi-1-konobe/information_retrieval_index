import os
import requests
import configs as c
from bs4 import BeautifulSoup
from tqdm import tqdm


class Parser:

    def run(self, stop_size):
        """
        парсим корпус документов
        :param stop_size: размер еорпуса в Мбайтах
        :return:
        """
        # переводим Мбайты в байты
        stop_size *= 1000000
        dir_size = 0
        # id статьи с которой начинаем парсить в порядке убывания
        id = c.START_ID
        dir_path = c.PATH_TO_CORPUS
        # визуализация прогресса
        pbar = tqdm(total=stop_size)
        while dir_size <= stop_size:
            article = self.get_article(id)
            if article:
                article_size = os.path.getsize(f'{dir_path}{article}')
                dir_size += article_size
                pbar.update(article_size)
            id -= 1
        pbar.close()

    @staticmethod
    def get_article(id):
        """
        проверяем наличие статьи по id, если статья есть, то сохраняем ее в txt-файле на диске
        :param id: id статьи
        :return: название сохраненного файла или False
        """
        # выгрузка документа
        req = requests.get('https://habr.com/ru/post/' + str(id) + '/')
        # парсинг документа
        soup = BeautifulSoup(req.text, 'html5lib')
        # если нет стать с таким id, то возвращаем False
        if not soup.find("span", {"class": "post__title-text"}):
            return False
        else:
            title = soup.find("span", {"class": "post__title-text"}).text
            text = soup.find("div", {"class": "post__text"}).text
            time = soup.find("span", {"class": "post__time"}).text

            file_name = f'{id}.txt'
            with open(f'corpus/{file_name}', 'w', encoding='utf-8') as f:
                f.write(f'ID: {id}\ntime: {time}\ntitle: {title}\ntext: {text}')

            return file_name






