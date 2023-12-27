# Создание индексной страницы блога с использованием Python и Open AI

Следующий сниппет на Python воспроизводит процесс чтения файлов статей блога, обращение к GPT-4 для генерации заголовка и краткого описания для каждого файла, а затем создания индексной страницы, содержащей ссылки на все статьи со сгенерированными заголовками и описаниями.

```python
import hashlib
import json
import os
import sys

from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm

from clients.openai import openai_client
```

Вначале импортируются необходимые для работы библиотеки. `hashlib` и `json` используются для работы с хэш-функциями и файлами JSON соответственно, `os` и `sys` – для работы с операционной системой, `jinja2` отвечает за работу с HTML-шаблонами, а `tqdm` позволяет отображать прогресс выполнения операций. `openai_client` это пользовательский класс, который предоставляет удобный интерфейс для взаимодействия с API OpenAI.

```python
from clients.openai import openai_client


def generate_title(file_path):
    ...
    response = openai_client.chat.completions.create(
        ...
        model="gpt-4",
    )
    return response.choices[0].message.content
```
Здесь функция `generate_title` использует GPT-4 для создания краткого заголовка файла Markdown. Входыми данными здесь является путь до файлика.

```python
def generate_summary(file_path):
    ...
    response = openai_client.chat.completions.create(
        ...
        model="gpt-4",
    )
    return response.choices[0].message.content
```

Функция `generate_summary` применяет модель генерации текста GPT-4 для создания краткого описания для файла Markdown.

```python
def hash_content(content):
    return hashlib.md5(content.encode()).hexdigest()
```

Функция `hash_content` использует md5 для создания хэш-значения содержимого файла. Это используется впоследствии для определения, был ли файл изменен или нет.

```python
def update_index(directory, index_path):
    ...
```

Функция `update_index` создает или обновляет индексный файл JSON для всех файлов Markdown в указанной директории. В этом JSON-файле для каждого файла Markdown хранится информация, требующаяся для генерации индексной страницы (путь к файлу, заголовок, описание и т.д.).

```python
@pysnooper.snoop()
def generate_index_md(json_path, output_md_path):
    ...
```

Функция `generate_index_md` берет данные из JSON-файла, который был сгенерирован или обновлен функцией `update_index`, и использует шаблонизатор Jinja2 для создания нового или обновления существующего Markdown-файла для главной страницы блога. Этот Markdown-файл содержит ссылки на все статьи блога со сгенерированными заголовками и описаниями.

```python
if __name__ == "__main__":
    ...
    try:
        update_index(blog_directory, index_data_path)
    except Exception as e:
        print(f"update_index failed with error: {e}")
        sys.exit(1)

    generate_index_md(index_data_path, index_file_path)
```

Эта часть кода выполняется, когда script запускается из командной строки. Сначала выполняется функция `update_index`, а затем `generate_index_md`.