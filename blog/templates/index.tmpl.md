# Индекс блога

{% if base %}
## Base
Раздел содержит основные материалы, вводные статьи про проект и общую информацию.
{% for file_info in base %}
- [{{ file_info.title or 'Без названия' }}](./{{ file_info.relative_path }}) : {{ file_info.summary }}
{% endfor %}
{% endif %}

{% if articles %}
## Articles
Раздел включает в себя статьи, подробно описывающие шаги проекта. Каждый этап проекта оформлен в виде отдельной статьи.
{% for file_info in articles %}
- [{{ file_info.title or 'Без названия' }}](./{{ file_info.relative_path }}) : {{ file_info.summary }}
{% endfor %}
{% endif %}


## Snippets
Раздел включает сниппеты, кои подробно объясняют код из использованных файлов и scripts.

{% if notebooks_snippets %}
### Auto Generated from Notebooks
Раздел включает сниппеты, сгенерированные автоматически из Jupyter Notebook файлов из директории `notebooks`
{% for file_info in notebooks_snippets %}
- [{{ file_info.title or 'Без названия' }}](./{{ file_info.relative_path }}) : {{ file_info.summary }}
{% endfor %}
{% endif %}

{% if python_snippets %}
### Auto Generated from Python
Раздел включает сниппеты, сгенерированные автоматически из Python файлов из директории `src`
{% for file_info in python_snippets %}
- [{{ file_info.title or 'Без названия' }}](./{{ file_info.relative_path }}) : {{ file_info.summary }}
{% endfor %}
{% endif %}
