import hashlib
import json
import os

from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm

from src.logic.generator.entity.summary import generate_summary
from src.logic.generator.entity.title import generate_title


def hash_content(content):
    """Возвращает хэш содержимого CONTENT, вычисленный с помощью алгоритма MD5."""
    return hashlib.md5(content.encode()).hexdigest()


def update_index(directory, index_path):
    """
    Обновляет данные индекса INDEX_DATA, если файлы в директории DIRECTORY изменились.
    """
    index_data = refresh_index(directory, index_path)

    pgbar = tqdm(index_data.items())
    for file_path, content_data in pgbar:
        if not content_data["is_updated"]:
            continue

        pgbar.set_description(f"Generating title and summary for {file_path}")

        index_data[file_path]["title"] = generate_title(file_path)
        index_data[file_path]["summary"] = generate_summary(file_path)

        # set is_updated=False to avoid re-generating title and summary
        index_data[file_path]["is_updated"] = False

    save_index(index_data, index_path)


def load_index(index_path):
    """
    Загружает данные индекса из JSON-файла INDEX_PATH.
    """
    if os.path.exists(index_path):
        with open(index_path, "r") as index_file:
            index_data = json.load(index_file)
    else:
        index_data = {}

    return index_data


def save_index(index_data, index_path):
    """
    Сохраняет данные индекса INDEX_DATA в JSON-файл INDEX_PATH.
    """
    with open(index_path, "w") as json_file:
        json.dump(index_data, json_file, indent=2, ensure_ascii=False)


def describe_md_file(directory):
    """
    Возвращает список всех файлов с расширением .md в директории DIRECTORY и ее поддиректориях.
    """
    all_md_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(directory)
        for file in files
        if file.endswith(".md") and file != "index.md"
    ]

    return all_md_files


def refresh_index(directory, index_path):
    """
    Обновляет данные индекса INDEX_DATA, обходя все файлы в BLOG_DIRECTORY.
    """
    index_data = load_index(index_path)
    all_md_files = describe_md_file(directory)

    for file_path in all_md_files:
        with open(file_path, "r") as file:
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

    return index_data


def serialize_index_data(index_data):
    """
    Сериализует данные индекса INDEX_DATA в словарь, содержащий только необходимые поля.
    """
    minified_index_data = {}
    for file_path, content_data in index_data.items():
        minified_index_data[file_path] = {
            "relative_path": content_data["relative_path"],
            "title": content_data["title"],
            "summary": content_data["summary"],
        }

    return minified_index_data


def sorted_index_data(index_data):
    """
    Возвращает отсортированные данные из индекса
    """
    return sorted(
        index_data.items(),
        key=lambda item: item[1]["relative_path"],
    )


def generate_index_md(json_path, output_md_path):
    """
    Генерирует файл index.md на основе данных индекса, используя jinja2-шаблон.
    """
    with open(json_path, "r") as json_file:
        data = json.load(json_file)

    context = {
        "00_base": [],
        "01_articles": [],
        "02_snippets/auto_generated/python/": [],
        "02_snippets/auto_generated/notebooks/": [],
    }

    for _, file_info in sorted_index_data(data):
        for context_key in context.keys():
            if context_key in file_info["relative_path"]:
                context[context_key].append(file_info)

    assert len(context["00_base"]) > 0
    assert len(context["01_articles"]) > 0
    assert len(context["02_snippets/auto_generated/python/"]) > 0
    assert len(context["02_snippets/auto_generated/notebooks/"]) > 0

    env = Environment(
        loader=FileSystemLoader("../../templates"),
    )
    template = env.get_template("index.tmpl.md")
    index_md_content = template.render(
        base=context["00_base"],
        articles=context["01_articles"],
        notebooks_snippets=context["02_snippets/auto_generated/notebooks/"],
        python_snippets=context["02_snippets/auto_generated/python/"],
    )

    with open(output_md_path, "w", encoding="utf-8") as md_file:
        md_file.write(index_md_content)
