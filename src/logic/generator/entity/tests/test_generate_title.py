import unittest
from unittest.mock import mock_open, patch

from src.logic.generator.entity.title import generate_title


class TestTitleGeneration(unittest.TestCase):
    @patch("src.logic.generator.entity.title.generate_from_prompt")
    @patch("src.logic.generator.entity.title.open", new_callable=mock_open, read_data="Test Article Content")
    def test_generate_title(self, mock_file, mock_generate_from_prompt):
        file_path = "test_article.md"
        expected_title = "Generated Title"

        mock_generate_from_prompt.return_value = expected_title

        result = generate_title(file_path)

        mock_file.assert_called_once_with(file_path, "r")
        mock_generate_from_prompt.assert_called_once_with(
            prompt_template_name="prompt/article_title_template.jinja2",
            prompt_template_params={
                "content": "Test Article Content",
            },
        )
        self.assertEqual(result, expected_title)


if __name__ == "__main__":
    unittest.main()
