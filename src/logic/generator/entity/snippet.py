from src.logic.generator.generative import generate_from_prompt


def generate_snippet(file_path):
    """
    Генерирует сниппет из файла с кодом через OpenAI API.
    :param file_path:
    :return:
    """
    with open(file_path, "r") as file:
        code = file.read()

    if not code:
        raise ValueError(f"File {file_path} is empty")

    snippet = generate_from_prompt(
        prompt_template_name="prompt/code_snippet_template.jinja2",
        prompt_template_params={
            "file_path": file_path,
            "code": code,
        },
    )

    return snippet
