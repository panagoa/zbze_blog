from src.logic.generator.generative import generate_from_prompt


def generate_summary(file_path):
    """
    Генерирует краткое описание статьи из файла с кодом через OpenAI API.
    """
    with open(file_path, "r") as file:
        content = file.read()

    if not content:
        return None

    # TODO: сделать генерацию более точной, прокинув в промпт "точечные" параметры контекста

    summary = generate_from_prompt(
        prompt_template_name="prompt/article_overview_template.jinja2",
        prompt_template_params={
            "content": content,
        },
    )

    return summary
