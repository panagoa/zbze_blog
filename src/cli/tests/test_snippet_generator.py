import os
import unittest
from unittest.mock import patch

from click.testing import CliRunner

from src.cli.snippet_generator import snippet_generator


class TestSnippetGenerator(unittest.TestCase):
    @patch("src.cli.snippet_generator.generate_snippet")
    def test_snippet_generator(self, mock_generate_snippet):
        mock_generate_snippet.return_value = "test result"

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open("test_file.txt", "w") as f:
                f.write("test")

            result = runner.invoke(snippet_generator, ["test_file.txt", "output.txt"])
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(os.path.exists("output.txt"))
            mock_generate_snippet.assert_called_once_with("test_file.txt")


if __name__ == "__main__":
    unittest.main()
