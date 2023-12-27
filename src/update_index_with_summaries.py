import hashlib
import json
import os
import sys

from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm

from clients.openai import openai_client


def generate_title(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    if not content:
        return None

    response = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": (
                    f"Создай краткий заголовок Markdown файла, находящегося по пути '{file_path}'. "
                    "Заголовок должен быть на русском языке, содержательным и точным, "
                    "4-6 слов должно быть достаточно.\n"
                    "Это будет заголовок статьи в блоге, Будет использоваться в качестве якоря для ссылки на статью. "
                    "Например:\n"
                    "[Очистка и предобработка текста](../auto_generated/notebooks/00_clean_scraped_text.md)\n"
                    f"\n\n"
                    f"```markdown\n{content}\n```\n\n"
                ),
            }
        ],
        model="gpt-4",
    )

    return response.choices[0].message.content


def generate_summary(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    if not content:
        return None

    response = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": (
                    f"Создай краткое описание для Markdown файла, находящегося по пути '{file_path}'. "
                    "Описание должно быть на русском языке, содержательным и точным. "
                    "Оно должно давать читателю ясное представление о содержании файла, его ключевых моментах и цели. "
                    "Описание длиной 1-2 предложением будет достаточно\n"
                    "Это будет описание статьи в блоге, будет использоваться в качестве краткого описания статьи. "
                    "Например:\n"
                    "[Очистка и предобработка текста](../auto_generated/notebooks/00_clean_scraped_text.md)\n"
                    "В этой статье мы рассмотрим как очистить и предобработать текст, "
                    "полученный в результате парсинга веб-страниц. "
                    "После этого текст можно будет использовать для дальнейшего анализа и обработки. \n"
                    "Ниже представлен исходный текст файла, для которого нужно создать описание. "
                    f"\n\n"
                    f"```markdown\n{content}\n```\n\n"
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
            "hash": current_hash,
            "is_updated": True,
            "content": content,
        }

    pgbar = tqdm(index_data.items())
    for file_path, content_data in pgbar:
        if not content_data["is_updated"]:
            continue

        pgbar.set_description(f"Generating title and summary for {file_path}")

        index_data[file_path]["title"] = generate_title(file_path)
        index_data[file_path]["summary"] = generate_summary(file_path)

        # set is_updated=False to avoid re-generating title and summary
        index_data[file_path]["is_updated"] = False

    with open(index_path, 'w') as json_file:
        json.dump(index_data, json_file, indent=2, ensure_ascii=False)


def serialize_index_data(index_data):
    minified_index_data = {}
    for file_path, content_data in index_data.items():
        minified_index_data[file_path] = {
            "relative_path": content_data["relative_path"],
            "title": content_data["title"],
            "summary": content_data["summary"],
        }

    return minified_index_data


def sorted_index_data(index_data):
    return sorted(
        index_data.items(),
        key=lambda item: item[1]["relative_path"],
    )


def generate_index_md(json_path, output_md_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

    context = {
        '00_base': [],
        '01_articles': [],
        '02_snippets/auto_generated/python/': [],
        '02_snippets/auto_generated/notebooks/': [],
    }

    for _, file_info in sorted_index_data(data):
        for context_key in context.keys():
            if context_key in file_info["relative_path"]:
                context[context_key].append(file_info)

    assert len(context['00_base']) > 0
    assert len(context['01_articles']) > 0
    assert len(context['02_snippets/auto_generated/python/']) > 0
    assert len(context['02_snippets/auto_generated/notebooks/']) > 0

    env = Environment(
        loader=FileSystemLoader('../blog/templates'),
    )
    template = env.get_template('index.tmpl.md')
    index_md_content = template.render(
        base=context['00_base'],
        articles=context['01_articles'],
        notebooks_snippets=context['02_snippets/auto_generated/notebooks/'],
        python_snippets=context['02_snippets/auto_generated/python/'],
    )

    with open(output_md_path, 'w', encoding='utf-8') as md_file:
        md_file.write(index_md_content)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update_index.py [blog_directory] [index_data_path]")
        sys.exit(1)

    blog_directory = sys.argv[1]
    index_data_path = sys.argv[2]
    index_file_path = os.path.join(blog_directory, "index.md")

    # try:
    #     update_index(blog_directory, index_data_path)
    # except Exception as e:
    #     print(f"update_index failed with error: {e}")
    #     sys.exit(1)

    generate_index_md(index_data_path, index_file_path)
