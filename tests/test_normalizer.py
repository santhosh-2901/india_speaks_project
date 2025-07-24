import unittest
import yaml
from pathlib import Path

# Adjust the path to import from the parent directory
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from india_speaks_cleaner.text_normalizer import normalize_text

class TestTextNormalizer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load the default config for testing
        config_path = Path(__file__).parent.parent / "india_speaks_cleaner/config.yaml"
        with open(config_path, 'r') as f:
            cls.config = yaml.safe_load(f)

    def test_english_normalization(self):
        text = "  This is a TEST sentence with the number 2024! "
        expected = "this is a test sentence with the number two zero two four!"
        self.assertEqual(normalize_text(text, 'en', self.config), expected)

    def test_english_punctuation_and_tokens(self):
        text = "Okay, what about this one? [laugh] It's great."
        expected = "okay, what about this one? [laugh] it's great."
        self.assertEqual(normalize_text(text, 'en', self.config), expected)

    def test_hindi_normalization(self):
        text = "Aaj ka din bahut achha hai"
        expected = "aj ka din bahut acha hai"
        self.assertEqual(normalize_text(text, 'hi', self.config), expected)

    def test_empty_and_whitespace_input(self):
        text = "   "
        expected = ""
        self.assertEqual(normalize_text(text, 'en', self.config), expected)

    def test_unsupported_language_uses_generic(self):
        # Generic normalization should still lowercase and clean whitespace/punctuation
        text = "  SOME Text with $$$ symbols  "
        expected = "some text with symbols"
        self.assertEqual(normalize_text(text, 'unsupported_lang', self.config), expected)

    def test_non_verbal_token_preservation(self):
        text = "This is a sentence [noise] with a token."
        expected = "this is a sentence [noise] with a token."
        self.assertEqual(normalize_text(text, 'en', self.config), expected)

if __name__ == '__main__':
    unittest.main()