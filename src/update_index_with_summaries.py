import hashlib
import json
import os
import re
import sys

from openai import OpenAI
from tqdm import tqdm

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def generate_summary(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    if not content:
        return None

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": (
                    f"Создай краткое описание для Markdown файла, находящегося по пути '{file_path}'. "
                    "Описание должно быть на русском языке, содержательным и точным. "
                    "Оно должно давать читателю ясное представление о содержании файла, его ключевых моментах и цели. "
                    "Описание должно быть написано в формате Markdown и подходить для использования в качестве "
                    "ссылочного описания в индексном файле блога. "
                    "Ниже представлен исходный текст файла, для которого нужно создать описание. "
                    f"\n\n"
                    f"```markdown\n{content}\n```\n\n"
                    "Сформируй описание, учитывая структуру и тему документа, используя ясный и краткий язык."
                ),
            }
        ],
        model="gpt-4",
    )

    return response.choices[0].message.content


def hash_content(content):
    return hashlib.md5(content.encode()).hexdigest()


def update_index(directory, index_path):
    if os.path.exists(index_path):
        with open(index_path, 'r') as index_file:
            index_data = json.load(index_file)
    else:
        index_data = {}

    all_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(directory)
        for file in files
        if file.endswith(".md") and file != 'index.md'
    ]

    for file_path in all_files:
        with open(file_path, 'r') as file:
            content = file.read()

        current_hash = hash_content(content)
        if file_path in index_data:
            if index_data[file_path]["hash"] == current_hash:
                print(f"Skipping {file_path} as it has not changed")
                continue

        relative_path = os.path.relpath(file_path, directory)
        index_data[file_path] = {
            "filename": os.path.basename(file_path),
            "path": file_path,
            "relative_path": relative_path,
            "title": extract_title(content),
            "hash": current_hash,
            "is_updated": True,
            "content": content,
        }

    pgbar = tqdm(index_data.items())
    for file_path, content_data in pgbar:
        if not content_data["is_updated"]:
            continue

        pgbar.set_description(f"Generating summary for {file_path}")
        summary = generate_summary(file_path)
        if summary:
            index_data[file_path]["summary"] = summary
            index_data[file_path]["is_updated"] = False

    with open(index_path, 'w') as json_file:
        json.dump(index_data, json_file, indent=2, ensure_ascii=False)


def extract_title(content):
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line.strip('# ').strip()
    return "Без названия"


def serialize_index_data(index_data):
    minified_index_data = {}
    for file_path, content_data in index_data.items():
        minified_index_data[file_path] = {
            "relative_path": content_data["relative_path"],
            "title": content_data["title"],
            "summary": content_data["summary"],
        }

    return minified_index_data


def generate_index_md(json_path, output_md_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

    minified_data = serialize_index_data(data)
    data = sorted(minified_data.items(), key=lambda x: x[1]["title"])

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": (
                    "Создай индексный файл для блога. "
                    "Индексный файл должен быть написан на русском языке, содержательным и точным. "
                    "Он должен давать читателю ясное представление о содержании блога, его ключевых моментах и цели. "
                    "Описание должно быть написано в формате Markdown и подходить для использования в качестве "
                    "ссылочного описания в индексном файле блога. "
                    "Структура записей блога такая: \n"
                    "- 00_base/ здесь лежат базовые материалы, вводные статьи про проект и т.д. \n"
                    "- 01_articles/ здесь лежат статьи, описывающие шаги проекта. "
                    "Конечный результат одной темы - одна статья. \n"
                    "- 02_snippets/ здесь лежат сниппеты, которые объясняют код из notebooks и python файлов. \n"
                    "-- auto_generated/notebooks - сниппеты, которые создаются автоматически из notebooks. \n"
                    "-- auto_generated/python - сниппеты, которые создаются автоматически из python файлов. \n"
                    "Короткие заметки с объяснением кода, идеи, и прочее из который потом можно собрать статью. \n"
                    "Ссылки на сниппеты должны быть разделены по папкам, в которых они лежат. \n"
                    "Чтобы читатель понимал разницу между сниппетами: \n"
                    "- которые созданы автоматически \n"
                    "-- из notebooks \n"
                    "-- из python файлов \n"
                    "- которые созданы вручную. \n"
                    "Ниже представлен исходный файл json, для которого нужно создать описание. "
                    f"\n\n"
                    f"```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```\n\n"
                    "Сформируй описание, учитывая структуру папок и темы документов, используя ясный и краткий язык."
                    "Раздели описание на несколько частей, по одной части на каждую папку. "
                    "Название папок нужно взять из путей к файлам из json по ключу 'relative_path'. "
                    "Сделай оформление максимально структурированным, чтобы читателю было удобно ориентироваться. "
                    "При этом, оформление должно быть красивым, с отступами и переносами строк. \n"
                    "Ссылки должны быть кликабельными, чтобы читатель мог перейти по ним. \n"
                    "Форматирование ссылок должно состоять из двух частей: \n"
                    "- ссылка на документ, название берется из имени файла. \n"
                    "- описание документа, можно взять из 'summary', но максимально короткое и лаконичное. \n" 
                    "Результат должен быть в формате Markdown, чтобы сразу сохратить его из python скрипта в файл. "
                ),
            }
        ],
        model="gpt-4",
    )

    content = response.choices[0].message.content
    pattern = r'```(?:markdown)?\n?(.*?)```'
    content = re.sub(pattern, r'\1', content, flags=re.DOTALL)

    with open(output_md_path, 'w') as output_file:
        output_file.write(content)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update_index.py [blog_directory] [index_data_path]")
        sys.exit(1)

    blog_directory = sys.argv[1]
    index_data_path = sys.argv[2]
    index_file_path = os.path.join(blog_directory, "index.md")

    try:
        update_index(blog_directory, index_data_path)
    except Exception as e:
        print(f"update_index failed with error: {e}")
        sys.exit(1)

    try:
        generate_index_md(index_data_path, index_file_path)
    except Exception as e:
        print(f"generate_index_md failed with error: {e}")
        sys.exit(1)