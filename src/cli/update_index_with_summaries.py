import os

import click

from src.logic.generator.entity.blog_index import generate_index_md, update_index


@click.command()
@click.argument("blog_directory", type=click.Path(exists=True))
@click.argument("index_data_path", type=click.Path())
def update_blog_index(blog_directory, index_data_path):
    """
    Обновляет индекс блога в BLOG_DIRECTORY, используя данные из INDEX_DATA_PATH.
    """
    index_file_path = os.path.join(blog_directory, "index.md")

    try:
        update_index(blog_directory, index_data_path)
    except Exception as e:
        click.echo(f"update_index failed with error: {e}", err=True)
        raise click.Abort()

    generate_index_md(index_data_path, index_file_path)


if __name__ == "__main__":
    update_blog_index()
