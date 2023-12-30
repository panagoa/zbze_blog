import unittest
from unittest.mock import mock_open, patch

from src.logic.generator.entity.summary import generate_summary


class TestSummaryGeneration(unittest.TestCase):
    @patch("src.logic.generator.entity.summary.generate_from_prompt")
    @patch("src.logic.generator.entity.summary.open", new_callable=mock_open, read_data="Test Article Content")
    def test_generate_summary(self, mock_file, mock_generate_from_prompt):
        file_path = "test_article.md"
        expected_summary = "Generated Summary"

        mock_generate_from_prompt.return_value = expected_summary

        result = generate_summary(file_path)

        mock_file.assert_called_once_with(file_path, "r")
        mock_generate_from_prompt.assert_called_once_with(
            prompt_template_name="prompt/article_overview_template.jinja2",
            prompt_template_params={
                "content": "Test Article Content",
            },
        )
        self.assertEqual(result, expected_summary)


if __name__ == "__main__":
    unittest.main()
