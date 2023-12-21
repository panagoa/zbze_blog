import os
import sys

from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def generate_snippet(file_path, output_path):
    with open(file_path, 'r') as file:
        code = file.read()

    if not code:
        raise ValueError(f"File {file_path} is empty")

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": (
                    f"Нужно создать сниппет объясняющий код из файла {file_path}. "
                    f"Сниппет должен быть написан на русском языке. "
                    f"Сниппет должен быть оформлен в формате Markdown. "
                    f"Сниппет должен быть коротким, но содержательным. "
                    f"Сниппет должен содержать исходный код и его объяснение. "
                    f"Сниппет нужен для того, чтобы человек, который не знаком с кодом, мог понять, что делает этот код."
                    f"Форматирование сниппета должно быть красивым, c отступами и переносами строк. "
                    f"Блоки с кодом должны быть выделены тремя апострофами, с указанием языка программирования. "
                    f"Стиль оформления сниппета должен быть как мини статья для блога, "
                    f"чтобы можно было собрать потом из нескольких сниппетов хорошую статью. "
                    f"Сам код из файла {file_path} представлен ниже в блоке кода."
                    f"\n\n"
                    f"```python\n{code}\n```\n\n"
                ),
            }
        ],
        model="gpt-4",
    )

    snippet = response.choices[0].message.content
    markdown_snippet = f"{snippet}"

    # Сохранение сниппета в файл
    with open(output_path, 'w') as output_file:
        output_file.write(markdown_snippet)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python snippet_generator.py [source_file_path] [output_markdown_path]")
        sys.exit(1)

    source_file_path = sys.argv[1]
    output_markdown_path = sys.argv[2]

    try:
        generate_snippet(source_file_path, output_markdown_path)
    except Exception as e:
        print(f"generate_snippet failed for {source_file_path} with error: {e}")
        sys.exit(1)
