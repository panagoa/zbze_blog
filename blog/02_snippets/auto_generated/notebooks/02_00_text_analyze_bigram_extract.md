# Анализ текста и извлечение биграмм с помощью Python и NLTK

Данный код позволяет исследовать связь между словами (более конкретно биграммами) в заданном текстовом файле. 
Биграмма – это пара последовательных слов в тексте.

## Чтение данных
Мы начинаем со стандартного импорта библиотек. Путь до файла указывается в переменной `file_path`. `BUF_SIZE` параметр, который контролирует сколько символов мы читаем из файла за одну итерацию. 
```python
import os
from collections import Counter
import nltk

file_dir = '../data/processed'
file_name = 'oshhamaho.txt'
file_path = os.path.join(file_dir, file_name)
BUF_SIZE = 100000
```

## Извлечение биграмм
```python
cnt = Counter()
with open(file_path) as f:
    tmp_raw = f.read(BUF_SIZE)
    while tmp_raw:
        tokens = nltk.word_tokenize(tmp_raw)
        text = nltk.Text(tokens)
        clc = text.collocation_list(5000)
        cnt.update(clc)
        tmp_raw = f.read(BUF_SIZE)
```
`nltk.word_tokenize` разбивает текст на отдельные слова. `nltk.Text` представляет текст как список слов. Метод `collocation_list` выдает наиболее частые биграмы текста. Результат сохраняется в `cnt`, который является объектом счетчика слов.

## Создание DataFrame
```python
import pandas as pd

data = [
    {
        'w_bigram': ' '.join(bigram),
        'freq': freq
    }
    for bigram, freq in cnt.items()
    if freq > 2
]

df = pd.DataFrame(data)
df = df.sort_values('freq', ascending=False)
```
Эти данные затем преобразуются в DataFrame для удобства просмотра и дальнейшей обработки.

## Сохранение данных
```python
df.to_csv(
    os.path.join('../data/processed/word_bigrams', file_name.replace('.txt', '.csv')),
    index=False,
)
```
DataFrame сохраняется в CSV файл.

## Проверка вероятности последовательности биграмм
```python
from nltk.probability import ConditionalFreqDist, ConditionalProbDist, MLEProbDist

cfdist = ConditionalFreqDist()

for bigram, freq in cnt.items():
    word1, word2 = bigram
    cfdist[word1][word2] = freq

cpdist = ConditionalProbDist(cfdist, MLEProbDist)
```
Здесь мы проверяем, насколько вероятно, что одно слово следует за другим.

## Получение вероятности для каждого слова
```python
def get_prob(word1):
    prob_dict = {}
    for word_2 in cpdist[word1].samples():
        prob_dict[word_2] = cpdist[word1].prob(word_2) * 100
    return prob_dict

sorted(get_prob('псалъэ').items(), key=lambda x: x[1], reverse=True)
```
`get_prob` возвращает словарь, показывающий, какие слова наиболее вероятно идут после данного слова. 

Такими способами мы можем проводить простой и исчерпывающий анализ текста. Код довольно прост, но позволяет получить полезную информацию о структуре текста и взаимосвязи слов в этом тексте.