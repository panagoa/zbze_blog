import os
import unittest

from src.logic.retrieval.code_entity_extractor import extract_descriptions


class TestCodeParsing(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(__file__)
        self.fixtures_dir = os.path.join(current_dir, "fixtures")
        fixture_path = os.path.join(self.fixtures_dir, "code_for_test_extract_names.py")

        with open(fixture_path, "r") as file:
            test_code = file.read()

        self.test_code = test_code

    def test_extract_descriptions(self):
        descriptions = extract_descriptions(self.test_code)
        self.assertEqual(
            descriptions,
            {
                "module_docstring": "Code for test_extract_names.py.",
                "imports": [
                    {"type": "Import", "names": ["os"]},
                    {"type": "ImportFrom", "module": "sys", "names": ["path as sys_path"]},
                    {"type": "Import", "names": ["backoff"]},
                ],
                "globals": [("FOO", "123")],
                "classes": [
                    {
                        "name": "MyClass",
                        "docstring": "MyClass docstring.",
                        "base_classes": [],
                        "methods": [
                            {"name": "method", "docstring": "Method docstring.", "signature": "method(self)"},
                            {
                                "name": "static_method",
                                "docstring": "Static method docstring.",
                                "signature": "static_method(a, b)",
                            },
                            {
                                "name": "class_method",
                                "docstring": "Class method docstring.",
                                "signature": "class_method(cls)",
                            },
                        ],
                        "attributes": ["class_attr"],
                    }
                ],
                "functions": [
                    {
                        "name": "foo",
                        "signature": "foo()",
                        "docstring": "Foo docstring.",
                        "decorators": ["backoff.on_exception(backoff.expo, Exception, max_tries=8)"],
                    },
                    {"name": "bar", "signature": "bar()", "docstring": "Bar docstring.", "decorators": []},
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
