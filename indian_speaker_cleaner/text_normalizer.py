import regex as re
import unicodedata
from unidecode import unidecode
from typing import Dict, Any
import pandas as pd

# A basic number to word converter for demonstration purposes
_NUM_TO_WORD_EN = {
    '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
    '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine',
    '10': 'ten', '11': 'eleven', '12': 'twelve', '13': 'thirteen', '14': 'fourteen',
    '15': 'fifteen', '16': 'sixteen', '17': 'seventeen', '18': 'eighteen', '19': 'nineteen'
}

_NUM_TO_WORD_HI = {
    '0': 'शून्य', '1': 'एक', '2': 'दो', '3': 'तीन', '4': 'चार',
    '5': 'पांच', '6': 'छह', '7': 'सात', '8': 'आठ', '9': 'नौ', '10': 'दस'
}

def _expand_numbers(text: str) -> str:
    """A simple regex-based number expander (demo)."""
    return re.sub(r'\d+', lambda m: _NUM_TO_WORD_EN.get(m.group(), m.group()), text)

def _clean_and_normalize_text(text: str, config: Dict[str, Any]) -> str:
    """Apply universal text cleaning rules."""
    text = str(text).lower().strip()
    text = unicodedata.normalize(config['text_params']['unicode_form'], text)

    # Preserve non-verbal tokens like [noise], [laugh] etc.
    non_verbal_tokens = re.findall(r'(\[\w+\])', text)
    text = re.sub(r'\[\w+\]', ' {} ', text)

    # Remove disallowed punctuation
    text = re.sub(config['text_params']['allowed_punctuation_regex'], "", text)
    
    # Restore non-verbal tokens
    for token in non_verbal_tokens:
        text = text.replace(' {} ', f' {token} ', 1)

    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def _normalize_english(text, config):
    if not isinstance(text, str):
        text = str(text) if not pd.isnull(text) else ""
    text = unidecode(text)
    text = _expand_numbers(text)
    return _clean_and_normalize_text(text, config)
def _normalize_hindi(text: str, config: Dict[str, Any]) -> str:
    """Normalizes Hindi text transliterated in Latin script."""
    if not isinstance(text, str):
        text = str(text) if text is not None else ""
        
    text = text.lower()
    # Normalize common variations as per spec (e.g., 'aa' -> 'a')
    text = re.sub(r'aa', 'a', text)
    text = re.sub(r'ee', 'i', text)
    text = re.sub(r'oo', 'u', text)
    # Basic number expansion would go here if Hindi numerals were present
    return _clean_and_normalize_text(text, config)
def _normalize_generic(text: str, config: Dict[str, Any]) -> str:
    """
    Apply generic normalization for languages where specific rules are not implemented.
    This serves as a placeholder for more complex transliteration/normalization.
    """
    return _clean_and_normalize_text(text, config)

# Dispatcher dictionary mapping language codes to normalization functions
NORMALIZATION_DISPATCHER = {
    'en': _normalize_english,
    'hi': _normalize_hindi,
    'bn': _normalize_generic,
    'ta': _normalize_generic,
    'te': _normalize_generic,
    'gu': _normalize_generic,
    'kn': _normalize_generic,
    'ml': _normalize_generic,
    'mr': _normalize_generic,
    'pa': _normalize_generic,
    'ur': _normalize_generic,
}

def normalize_text(text: str, language: str, config: Dict[str, Any]) -> str:
    """
    Top-level function to normalize a transcript based on its language.

    Args:
        text (str): The raw transcription text.
        language (str): The language code (e.g., 'hi', 'en').
        config (Dict[str, Any]): The configuration dictionary.

    Returns:
        str: The normalized transcription.
    """
    normalizer_func = NORMALIZATION_DISPATCHER.get(language, _normalize_generic)
    return normalizer_func(text, config)