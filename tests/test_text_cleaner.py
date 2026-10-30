import unittest

from src.preprocessing.text_cleaner import clean_text


class TestTextCleaner(unittest.TestCase):

    def test_extra_spaces(self):
        self.assertEqual(
            clean_text("Ashoka    was    an emperor"),
            "Ashoka was an emperor"
        )

    def test_leading_trailing_spaces(self):
        self.assertEqual(
            clean_text("  Ancient India  "),
            "Ancient India"
        )

    def test_empty_text(self):
        self.assertEqual(clean_text(""), "")

    def test_preserve_punctuation(self):
        self.assertEqual(
            clean_text("Ashoka, Emperor of India!"),
            "Ashoka, Emperor of India!"
        )

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            clean_text(None)


if __name__ == "__main__":
    unittest.main()