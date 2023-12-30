import os
import sys

import click

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cli.snippet_generator import snippet_generator
from cli.update_index_with_summaries import update_blog_index


@click.group()
def cli():
    pass


cli.add_command(snippet_generator)
cli.add_command(update_blog_index)

if __name__ == "__main__":
    cli()
