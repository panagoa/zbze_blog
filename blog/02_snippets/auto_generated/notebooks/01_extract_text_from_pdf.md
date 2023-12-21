## Извлечение текста из PDF файла с помощью Python

Python обладает множеством библиотек, с помощью которых можно обрабатывать различные типы файлов. В данном сниппете мы рассмотрим как извлечь текст из PDF файлов и сохранить его в txt файлы с помощью модулей `textract`, `os` и `tqdm`.

Прежде всего, с помощью модуля `os` создаётся папка для сохранения текстовых файлов.

```python
oshhamaho_external_pdf_dir = '../data/external/oshhamaho'
oshhamaho_interim_txt_dir = '../data/interim/oshhamaho'
os.makedirs(oshhamaho_interim_txt_dir, exist_ok=True)

pdf_files = [f for f in os.listdir(oshhamaho_external_pdf_dir) if f.endswith('.pdf')]
```

Затем определена функция `extract_text_from_pdf_file()`, которая берёт на вход путь к PDF файлу, извлекает из него текст и возвращает этот текст в виде строки, с использованием библиотеки `textract`.

```python
import textract
def extract_text_from_pdf_file(pdf_path):
    try:
        text = textract.process(pdf_path, method='pdfminer')
    except Exception:
        return ''
    text = text.decode('utf-8')
    return text
```

Циклом пробегаем по всем файлам с расширением '.pdf', извлекаем текст и сохраняем как текстовый файл '.txt'.

```python
pgbar = tqdm(pdf_files)

for pdf_file in pgbar:
    pgbar.set_description(pdf_file)
    pdf_path = os.path.join(oshhamaho_external_pdf_dir, pdf_file)
    
    text_i = extract_text_from_pdf_file(pdf_path)
    cleaned_text = clean_text(text_i) 

    text_file = pdf_file.replace('.pdf', '.txt')
    text_path = os.path.join(oshhamaho_interim_txt_dir, text_file)
    
    with open(text_path, 'w') as f:
        f.write(cleaned_text)
```

В данном коде используется `tqdm` для создания интерактивной строки прогресса. Это не обязательно, но увеличивает удобство работы.

Затем из каждого текстового файла текст собирается, очищается и склеивается в одну большую строку, после чего записывается в новый файл.

```python
txt_files = sorted([f for f in os.listdir(oshhamaho_interim_txt_dir) if f.endswith('.txt')])
processed_dir = '../data/processed/'
os.makedirs(processed_dir, exist_ok=True)

oshhamaho_all_txt_path = os.path.join(processed_dir, 'oshhamaho.txt')

pgbar = tqdm(txt_files)
text = ''

for txt_file in pgbar:
    pgbar.set_description(txt_file)
    txt_path = os.path.join(oshhamaho_interim_txt_dir, txt_file)
    
    with open(txt_path, 'r') as f:
        text_i = f.read()
    
    cleaned_text = clean_text(text_i) 
    text += cleaned_text + '\n'

with open(oshhamaho_all_txt_path, 'w') as f:
    f.write(text)
```
Этот код можно использовать для автоматизации процесса извлечения текста из большого количества PDF файлов. Он легко модифицируется в соответствии с требованиями вашего проекта.