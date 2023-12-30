from src.logic.generator.generative import generate_from_prompt


def generate_title(file_path):
    """
    Генерирует заголовок статьи из файла с кодом через OpenAI API.
    :param file_path:
    :return:
    """
    with open(file_path, "r") as file:
        content = file.read()

    if not content:
        return None

    # TODO: сделать генерацию более точной, прокинув в промпт "точечные" параметры контекста.
    #  Попытаться уменьшить контекст, чтобы зря не тратить лимиты гоняя весь файл.
    title = generate_from_prompt(
        prompt_template_name="prompt/article_title_template.jinja2",
        prompt_template_params={
            "content": content,
        },
    )

    return title
