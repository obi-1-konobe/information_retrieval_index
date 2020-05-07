import os
import random
from typing import List
import torch
import pandas as pd
import numpy as np
import transformers as ppb
from scipy import spatial
from rank import RankList as rl

import configs as c
"""
модуль демонстрирует поиск дубликатов
"""

# инициализируем NLP пакеты
model_class, tokenizer_class, pretrained_weights = (
    ppb.DistilBertModel,
    ppb.DistilBertTokenizer,
    'distilbert-base-uncased'
)
tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
model = model_class.from_pretrained(pretrained_weights)
# случайно выбираем 100 документов из корпуса
listdir: List[str] = os.listdir(f'{c.PATH_TO_CORPUS}')
doc_list: List[str] = random.sample(listdir, 100)

data = list()
for doc in doc_list:
    doc_path: str = f'{c.PATH_TO_CORPUS}{doc}'
    with open(doc_path, 'r') as f:
        text: str = f.read()
    data.append([doc, text])

# выбираем 10 документов и создаем для них дубликаты
for doc in doc_list[:10]:
    doc_path: str = f'{c.PATH_TO_CORPUS}{doc}'
    with open(doc_path, 'r') as f:
        text: str = f.read()
    data.append([f'duplicate_{doc}', text])
# объединяем данные в датафреим
df = pd.DataFrame(data, columns=['file', 'text'])
# перемешиваем строки в датафреиме
df = df.sample(frac=1)
# токенизируем тексты
tokenized = df['text'].apply(
    lambda x: tokenizer.encode(x, add_special_tokens=True)
)
# выравниваем длины массивов
padded = rl.zero_padding(tokenized)
# проаускаем данные через BERT
input_ids = torch.tensor(np.array(padded))
with torch.no_grad():
    last_hidden_states = model(input_ids)
# получаем эмбединги текстов
features = last_hidden_states[0][:, 0, :].numpy()
# создвем словарь с дубликатами
duplicates = dict()
for i in range(features.shape[0]):
    for j in range(features.shape[0]):
        if i != j:
            cos_similarity: float = 1 - spatial.distance.cosine(
                features[i], features[j]
            )
            if cos_similarity > 0.99:
                file_i: str = df.file.values[i]
                file_j: str = df.file.values[j]
                duplicates[file_i] = file_j
# вывод результатов
for key in duplicates:
    print(key, duplicates[key])
