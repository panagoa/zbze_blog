import unittest
from unittest.mock import mock_open, patch

from src.logic.generator.entity.snippet import generate_snippet


class TestSnippetGeneration(unittest.TestCase):
    @patch("src.logic.generator.entity.snippet.generate_from_prompt")
    @patch("src.logic.generator.entity.snippet.open", new_callable=mock_open, read_data="Test Code")
    def test_generate_snippet(self, mock_file, mock_generate_from_prompt):
        file_path = "test_file.py"
        expected_snippet = "Generated Snippet"

        mock_generate_from_prompt.return_value = expected_snippet

        result = generate_snippet(file_path)

        mock_file.assert_called_once_with(file_path, "r")
        mock_generate_from_prompt.assert_called_once_with(
            prompt_template_name="prompt/code_snippet_template.jinja2",
            prompt_template_params={
                "file_path": file_path,
                "code": "Test Code",
            },
        )
        self.assertEqual(result, expected_snippet)


if __name__ == "__main__":
    unittest.main()
