import datetime
import os

from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateNotFound
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser

from src.settings import PROMPTS_DEBUG_DIR, TEMPLATE_DIR


def fill_prompt(template_name, template_params, path_to_templates=TEMPLATE_DIR):
    """
    Готовит промпт для генерации на основе jinja2-шаблона и контекста
    """
    loader = FileSystemLoader(path_to_templates)
    env = Environment(
        loader=loader,
        undefined=StrictUndefined,
    )

    try:
        template = env.get_template(template_name)
    except TemplateNotFound as e:
        print(e, path_to_templates)
        print(loader.list_templates())
        raise

    try:
        prompt = template.render(**template_params)
    except Exception as e:
        print(f"Rendering template {template_name} failed with error: {e} with params: {template_params}")
        raise e

    prompt_debug_dump = os.path.join(PROMPTS_DEBUG_DIR, template_name)
    os.makedirs(prompt_debug_dump, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(os.path.join(prompt_debug_dump, f"{timestamp}.md"), "w") as f:
        f.write(prompt)

    return prompt


def generate_from_prompt(
    prompt_template_name,
    prompt_template_params,
    path_to_templates=TEMPLATE_DIR,
    model_name="gpt-3.5-turbo",
    prompt_debug=True,
):
    """
    Генерирует текст на основе промпта, используя OpenAI API.
    """
    prompt_string = fill_prompt(
        template_name=prompt_template_name,
        template_params=prompt_template_params,
        path_to_templates=path_to_templates,
    )

    prompt = ChatPromptTemplate.from_messages(
        messages=[
            HumanMessage(
                content=prompt_string,
            ),
        ]
    )
    model = ChatOpenAI(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        model_name=model_name,
    )
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser
    if prompt_debug:
        chain = prompt

    result = chain.invoke(input=None)
    output = result.to_string()
    return output
