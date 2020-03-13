"""
модуль содержит константы и тригеры для конфигурации программы
"""

from typing import List
# main

CORPUS_PARSER: bool = False
BUILD_INDEX: bool = False
STOP_DOWNLOAD_SIZE: int = 50
SEPARATOR: str = '*' * 30 + '\n'

# my_parser
START_ID: int = 489734
PATH_TO_CORPUS: str = 'corpus/'

# spimi
MEMORY_SIZE: int = 10**6
INDEX_DIR: str = 'index/'
TEMP_DIR: str = 'temp/'

# preprocess
OPERATORS: List[str] = ['AND', 'OR', 'NOT']
