import unittest
from unittest.mock import mock_open, patch

from src.logic.generator.generative import fill_prompt, generate_from_prompt


class TestTextGeneration(unittest.TestCase):
    @patch("src.logic.generator.generative.fill_prompt")
    @patch("src.logic.generator.generative.ChatOpenAI")
    def test_generate_from_prompt(self, mock_chat_openai, mock_fill_prompt):
        expected_prompt = "test prompt"
        expected_response = "generated text"

        template_name = "test_template"
        template_params = {"param1": "value1"}
        path_to_templates = "path/to/templates"
        model_name = "gpt-3.5-turbo"
        mock_fill_prompt.return_value = expected_prompt
        mock_chat_openai.return_value.invoke.return_value.to_string.return_value = expected_response

        output = generate_from_prompt(template_name, template_params, path_to_templates, model_name, prompt_debug=True)

        mock_fill_prompt.assert_called_with(
            template_name=template_name,
            template_params=template_params,
            path_to_templates=path_to_templates,
        )
        self.assertEqual(output, f"Human: {expected_prompt}")

    @patch("src.logic.generator.generative.os")
    @patch("src.logic.generator.generative.open", new_callable=mock_open, read_data="test prompt")
    def test_fill_prompt_article_title_template(self, mock_file, mock_os):
        expected_file_path = "path/to/file"
        expected_keywords = ["keyword1", "keyword2"]
        expected_content_ast = "test content ast"

        template_name = "prompt/article_title_template.jinja2"
        template_params = {
            "file_path": expected_file_path,
            "keywords": expected_keywords,
            "content_ast": expected_content_ast,
        }

        prompt = fill_prompt(template_name, template_params)

        mock_file.assert_called()
        self.assertIn(
            f"Создай краткий заголовок для Markdown файла, находящегося по пути '{expected_file_path}'.", prompt
        )
        self.assertIn("Предлагаемые ключевые слова или фразы из содержимого:\n- keyword1\n- keyword2", prompt)
        self.assertIn(f"содержимое файла.\n```json\n{expected_content_ast}\n```", prompt)


if __name__ == "__main__":
    unittest.main()
