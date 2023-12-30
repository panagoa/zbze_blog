import hashlib
import json
import os
import unittest
from unittest import mock
from unittest.mock import MagicMock, mock_open, patch

from src.logic.generator.entity.blog_index import (
    generate_index_md,
    hash_content,
    serialize_index_data,
    sorted_index_data,
    update_index,
)


class TestBlogFunctions(unittest.TestCase):
    def test_hash_content(self):
        test_content = "Hello, World!"
        expected_hash = hashlib.md5(test_content.encode()).hexdigest()
        self.assertEqual(hash_content(test_content), expected_hash)

    @patch("src.logic.generator.entity.blog_index.json.dump")
    @patch("src.logic.generator.entity.blog_index.open", new_callable=mock_open, read_data="Test Content")
    @patch("src.logic.generator.entity.blog_index.os")
    def test_update_index(self, mock_os, mock_file, mock_json_dump):
        mock_json_load = MagicMock()
        mock_json_load.return_value = {
            "test_file1.md": {
                "filename": "test_file1.md",
                "path": "test_file1.md",
                "relative_path": "test_file1.md",
                "hash": "fc3934bf4a02d43ef4773acf9e87f0bc",
                "is_updated": False,
                "content": "",
            },
        }
        with patch("src.logic.generator.entity.blog_index.json.load", mock_json_load):
            update_index("test_directory", "test_index_path")

        mock_os.walk.assert_called_with("test_directory")
        self.assertEqual(mock_file.call_count, 2)
        mock_json_load.assert_called_once()
        mock_json_dump.assert_called_once()

    def test_serialize_index_data(self):
        test_index_data = {
            "test_path": {
                "relative_path": "path/to/test",
                "title": "Test Title",
                "summary": "Test Summary",
                "extra_field": "extra_value",
            }
        }
        expected_result = {
            "test_path": {"relative_path": "path/to/test", "title": "Test Title", "summary": "Test Summary"}
        }
        self.assertEqual(serialize_index_data(test_index_data), expected_result)

    def test_sorted_index_data(self):
        test_index_data = {
            "path2": {"relative_path": "00_b"},
            "path3": {"relative_path": "02_c"},
            "path1": {"relative_path": "01_a"},
        }
        expected_order = [
            ("path2", {"relative_path": "00_b"}),
            ("path1", {"relative_path": "01_a"}),
            ("path3", {"relative_path": "02_c"}),
        ]
        self.assertEqual(sorted_index_data(test_index_data), expected_order)

    @patch("src.logic.generator.entity.blog_index.Environment")
    def test_generate_index_md(self, mock_environment):
        relative_paths = [
            "00_base/01_introduction.md",
            "01_articles/how_to_write_a_blog_post.md",
            "02_snippets/auto_generated/python/01_test_snippet.md",
            "02_snippets/auto_generated/notebooks/01_test_notebook.md",
        ]

        test_data = {
            f"../blog/{relative_path}": {
                "filename": os.path.basename(relative_path),
                "path": f"../blog/{relative_path}",
                "relative_path": relative_path,
                "hash": "fc3934bf4a02d43ef4773acf9e87f0bc",
                "is_updated": False,
                "content": "",
                "title": "",
                "summary": "",
            }
            for relative_path in relative_paths
        }

        mock_file = mock_open(read_data=json.dumps(test_data))

        mock_template = MagicMock()
        mock_environment.return_value.get_template.return_value = mock_template

        with patch("src.logic.generator.entity.blog_index.open", mock_file):
            generate_index_md("test_json_path", "test_output_md_path")

            expected_calls = [
                mock.call("test_json_path", "r"),
            ]
            mock_file.assert_has_calls(expected_calls)

            mock_environment.return_value.get_template.assert_called_once_with("index.tmpl.md")
            mock_template.render.assert_called_once()


if __name__ == "__main__":
    unittest.main()
