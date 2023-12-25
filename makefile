NOTEBOOK_DIR := notebooks/
PYTHON_SRC_DIR := src/
AUTO_GEN_SNIPPET_DIR := blog/02_snippets/auto_generated/

MODE ?= diff

ifeq ($(MODE),all)
    NOTEBOOKS := $(wildcard $(NOTEBOOK_DIR)*.ipynb)
    PYTHON_FILES := $(wildcard $(PYTHON_SRC_DIR)*.py)
    $(info Выбран режим: Все файлы)
else ifeq ($(MODE),diff)
    CHANGED_NOTEBOOKS := $(shell git diff --name-only HEAD | grep "$(NOTEBOOK_DIR).*\.ipynb")
    CHANGED_PYTHON_FILES := $(shell git diff --name-only HEAD | grep "$(PYTHON_SRC_DIR).*\.py")
    NOTEBOOKS := $(CHANGED_NOTEBOOKS)
    PYTHON_FILES := $(CHANGED_PYTHON_FILES)
    $(info Выбран режим: Измененные файлы)
else
    $(error Неизвестный режим: $(MODE))
endif


all: clean_deleted create_dirs notebooks_snippets python_snippets

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

DELETED_FILES := $(shell git diff --name-status HEAD | grep 'D\t' | cut -f2 | grep -E '$(NOTEBOOK_DIR)|$(PYTHON_SRC_DIR)')

clean_deleted:
	@echo "Очистка сгенерированных файлов, для файлов, которые были удалены или переименованы..."
	@$(foreach file,$(DELETED_FILES),\
	    $(if $(findstring $(NOTEBOOK_DIR),$(file)),\
	        rm -f $(AUTO_GEN_SNIPPET_DIR)notebooks/$(notdir $(file:.ipynb=.md));,\
	    $(if $(findstring $(PYTHON_SRC_DIR),$(file)),\
	        rm -f $(AUTO_GEN_SNIPPET_DIR)python/$(notdir $(file:.py=.md));)))
