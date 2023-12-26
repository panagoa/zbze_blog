# Анализ частоты слов сравнение по источникам

Этот сниппет иллюстрирует процесс анализа частоты слов в текстах из разных источников. Анализ проводится на примере трех отдельных датасетов, которые содержат информацию о частоте слов.

## Загрузка данных
Исходные датасеты загружаются при помощи функции pandas read_csv.

```python
import os
import pandas as pd

input_dir = '../data/processed/word_freqs'

df_freq_apkbr_ru = pd.read_csv(os.path.join(input_dir, 'freq_1000000_apkbr_ru.csv'))
df_freq_elgkbr_ru = pd.read_csv(os.path.join(input_dir, 'freq_1000000_elgkbr_ru.csv'))
df_freq_oshhamaho = pd.read_csv(os.path.join(input_dir, 'freq_1000000_oshhamaho.csv'))
```
## Подсчет топа слов
В следующем блоке кода вычисляются топ-100 самых часто встречающихся слов для каждого из датасетов.

```python
top_count = 100
df_freq_apkbr_ru_top = df_freq_apkbr_ru.sort_values(by='freq', ascending=False).head(top_count)
df_freq_elgkbr_ru_top = df_freq_elgkbr_ru.sort_values(by='freq', ascending=False).head(top_count)
df_freq_oshhamaho_top = df_freq_oshhamaho.sort_values(by='freq', ascending=False).head(top_count)
```
## Подсчет уникальных слов
Далее для каждого источника вычисляются уникальные слова, которые встречаются только в том определенном источнике и отсутствуют в двух других.

```python
apkbr_ru = df_freq_apkbr_ru_top.merge(
    df_freq_elgkbr_ru_top, 
    how='left', 
    left_on='word', 
    right_on='word', 
    suffixes=('_apkbr_ru', '_elgkbr_ru')
).merge(
    df_freq_oshhamaho_top, 
    how='left', 
    left_on='word', 
    right_on='word', 
)
apkbr_ru.rename(columns={'freq': 'freq_oshhamaho'}, inplace=True)
apkbr_ru_uniq = apkbr_ru[
    (apkbr_ru.freq_elgkbr_ru.isna()) & 
    (apkbr_ru.freq_oshhamaho.isna())
]
```
Аналогично для остальных источников.

## Заключение

В результате построена таблица топ-100 уникальных слов для каждого источника. На основе этих данных можно делать выводы о характерных особенностях каждого источника. В частности, это может быть полезно при анализе тематической спецификации текстов.