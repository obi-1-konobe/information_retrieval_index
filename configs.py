"""
модуль содержит константы и тригеры для конфигурации программы
"""

from typing import List

# main
CORPUS_PARSER: bool = False
BUILD_INDEX: bool = False
SEPARATOR: str = '*' * 30 + '\n'

# my_parser
PATH_TO_CORPUS: str = 'corpus/texts/'

# spimi
MEMORY_SIZE: int = 10**6
INDEX_DIR: str = 'index/'
TEMP_DIR: str = 'temp/'

# preprocess
OPERATORS: List[str] = ['AND', 'OR', 'NOT']
