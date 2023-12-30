import click

from src.logic.generator.entity.snippet import generate_snippet


@click.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def snippet_generator(file_path, output_path):
    """
    Генерирует сниппет из файла с кодом FILE_PATH и сохраняет его в OUTPUT_PATH.
    """
    snippet = generate_snippet(file_path)

    with open(output_path, "w") as output_file:
        output_file.write(snippet)


if __name__ == "__main__":
    snippet_generator()
