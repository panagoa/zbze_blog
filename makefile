NOTEBOOK_DIR := notebooks/
PYTHON_SRC_DIR := src/
AUTO_GEN_SNIPPET_DIR := blog/02_snippets/auto_generated/

NOTEBOOKS := $(wildcard $(NOTEBOOK_DIR)*.ipynb)
PYTHON_FILES := $(wildcard $(PYTHON_SRC_DIR)*.py)

all: create_dirs notebooks_snippets python_snippets
# todo gen only changed files
# todo add gen to pre-commit hook
#all: create_dirs notebooks_snippets python_snippets
#gen_diff: create_dirs notebooks_snippets python_snippets
#gen_all: create_dirs notebooks_snippets python_snippets


create_dirs:
	@echo "Создание директорий для сниппетов..."
	@mkdir -p $(AUTO_GEN_SNIPPET_DIR)notebooks
	@mkdir -p $(AUTO_GEN_SNIPPET_DIR)python

notebooks_snippets:
	@echo "Генерация сниппетов из Jupyter Notebooks..."
	@cd $(NOTEBOOK_DIR); \
	$(foreach nb, $(NOTEBOOKS), \
	    OUTPUT_MD="../$(AUTO_GEN_SNIPPET_DIR)notebooks/$(notdir $(nb:.ipynb=.md))"; \
	    echo "Преобразование $(nb) в Markdown, выходной файл: $$OUTPUT_MD..."; \
	    jupyter nbconvert --to markdown $(notdir $(nb)) --output $$OUTPUT_MD; \
	    python ../$(PYTHON_SRC_DIR)snippet_generator.py $$OUTPUT_MD $$OUTPUT_MD; \
	)

python_snippets:
	@echo "Генерация сниппетов из Python файлов..."
	@$(foreach py, $(PYTHON_FILES), \
	    OUTPUT_MD="$(AUTO_GEN_SNIPPET_DIR)python/$(notdir $(py:.py=.md))"; \
	    echo "Обработка файла $(py), выходной файл: $$OUTPUT_MD..."; \
	    python $(PYTHON_SRC_DIR)snippet_generator.py $(py) $$OUTPUT_MD; \
	)

clean:
	@echo "Очистка сгенерированных файлов..."
	@rm -rf $(AUTO_GEN_SNIPPET_DIR)
