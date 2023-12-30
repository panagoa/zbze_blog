import os
import unittest
from unittest.mock import patch

from click.testing import CliRunner

from src.cli.update_index_with_summaries import update_blog_index


class TestUpdateBlogIndex(unittest.TestCase):
    @patch("src.cli.update_index_with_summaries.update_index")
    @patch("src.cli.update_index_with_summaries.generate_index_md")
    def test_update_blog_index(self, mock_generate_index_md, mock_update_index):
        runner = CliRunner()

        with runner.isolated_filesystem():
            os.mkdir("blog_directory")
            with open(os.path.join("blog_directory", "index_data.txt"), "w") as f:
                f.write("test")

            result = runner.invoke(update_blog_index, ["blog_directory", "index_data.txt"])

            self.assertEqual(result.exit_code, 0)

            mock_update_index.assert_called_once_with("blog_directory", "index_data.txt")
            mock_generate_index_md.assert_called_once_with("index_data.txt", os.path.join("blog_directory", "index.md"))


if __name__ == "__main__":
    unittest.main()
