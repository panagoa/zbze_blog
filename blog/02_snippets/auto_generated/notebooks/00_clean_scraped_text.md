# Очистка и предобработка текста

В этом модуле Python мы будем использовать numpy, pandas и os для считывания, очистки и сохранения данных, полученных в результате web-скрейпинга.

```python
import os  # библиотека для работы с файлами и папками
import pandas as pd  # библиотека для работы с таблицами данных
from src.logic.text_cleaner import clean_text  # функция для очистки текста
```

Этот код используется для импорта необходимых библиотек и функций.

```python
external_dir = '../data/external/'
interim_dir = '../data/interim/'
os.makedirs(interim_dir, exist_ok=True)

processed_dir = '../data/processed/'
os.makedirs(processed_dir, exist_ok=True)
```

Мы создаем папку для сохранения данных после очистки.

```python
for file_name in ['apkbr_ru.jsonl', 'elgkbr_ru.jsonl']:    
    df = pd.read_json(os.path.join(external_dir, file_name), lines=True)
    df['content'] = df['content'].apply(clean_text)
```

Этот код обрабатывает файлы json. Он загружает каждый файл в DataFrame (df), затем применяет функцию clean_text к каждой строке в колонке 'content'.

```python
df.to_json(
        os.path.join(interim_dir, file_name), 
        orient='records', 
        lines=True,
        force_ascii=False
    )
```

После очистки данные сохраняются обратно в json-файл.

```python
text = '\n'.join(df['content'].tolist())
    with open(os.path.join(processed_dir, file_name.replace('.jsonl', '.txt')), 'w') as f:
        f.write(text)
```

Здесь содержимое каждой строки объединяется в одну большую строку, которая затем сохраняется в файл .txt. 

Итак, этот сниппет берет необработанные данные, полученные из веб-скрапинга, и чистит их от нестандартных символов и пробелов, чтобы подготовить их к дальнейшей обработке. После очистки данные сохраняются в двух форматах - .json и .txt.