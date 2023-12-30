import unittest

from src.logic.text_cleaner import (
    add_space_after_comma,
    clean_encoding,
    clean_text,
    remove_emojis,
    remove_garbage,
    remove_html_tags,
    remove_i_sections,
    remove_many_dot,
    remove_many_spaces,
    remove_non_whitelisted_chars,
    remove_redundant_punctuation,
    remove_spaced_letters,
    remove_uppercase_words,
    remove_word_with_ii,
    replace_many_newlines_with_one,
    replace_spaces_before_punctuation,
    unify_hyphenated_words,
)


class TestTextCleaning(unittest.TestCase):
    def test_clean_encoding(self):
        self.assertEqual(clean_encoding("(cid:123)* * *(cid:456)"), "")

    def test_remove_i_sections(self):
        self.assertEqual(remove_i_sections("Iуащхьэмахуэ(i:123)"), "Iуащхьэмахуэ")

    def test_remove_uppercase_words(self):
        self.assertEqual(remove_uppercase_words("IУАЩХЬЭМАХУЭ"), "")

    def test_replace_many_newlines_with_one(self):
        self.assertEqual(replace_many_newlines_with_one("КIэщIу\n\n\nжыпIэмэ"), "КIэщIу\nжыпIэмэ")

    def test_replace_spaces_before_punctuation(self):
        self.assertEqual(replace_spaces_before_punctuation("Hello , world !"), "Hello, world!")

    def test_remove_word_with_ii(self):
        self.assertEqual(remove_word_with_ii("IIшэдджыжь щIыIэ"), " щIыIэ")

    def test_add_space_after_comma(self):
        self.assertEqual(add_space_after_comma("Hello,world"), "Hello, world")

    def test_remove_many_spaces(self):
        self.assertEqual(remove_many_spaces("Хьэндыркъуакъуэ  щIакъуэр"), "Хьэндыркъуакъуэ щIакъуэр")

    def test_remove_many_dot(self):
        self.assertEqual(remove_many_dot("уэху..."), "уэху.")

    def test_remove_html_tags(self):
        self.assertEqual(remove_html_tags("<p>This is a test</p>"), "This is a test")

    def test_remove_emojis(self):
        self.assertEqual(remove_emojis("Hello 😊"), "Hello ")

    def test_remove_redundant_punctuation(self):
        self.assertEqual(remove_redundant_punctuation("Hello!!"), "Hello!")

    def test_remove_spaced_letters(self):
        self.assertEqual(remove_spaced_letters("П ы х у с ы х у"), "")

    def test_remove_non_whitelisted_chars(self):
        self.assertEqual(remove_non_whitelisted_chars("Къэбэрдей-Балъкъэр kbr"), "Къэбэрдей-Балъкъэр ")

    def test_unify_hyphenated_words(self):
        self.assertEqual(unify_hyphenated_words("Iуащхьэ-\nмахуэ"), "Iуащхьэмахуэ")

    def test_remove_garbage(self):
        self.assertEqual(remove_garbage(", : I ? I I, I I! > I I I I. : «, .!» I I, . I, I, , I I, I., I I, , . I"), "")

    def test_clean_text_integration(self):
        test_text = '(cid:123)Электронная газета "Адыгэ псалъэ" \n\n<a>apkbr.ru</a>(i:123) \n\n'
        expected_text = "Электронная газета Адыгэ псалъэ. "
        self.assertEqual(clean_text(test_text), expected_text)


if __name__ == "__main__":
    unittest.main()
