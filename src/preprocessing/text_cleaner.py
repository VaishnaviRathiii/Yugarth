import re
import unicodedata


def clean_text(text):
    """
    Clean historical text while preserving
    meaningful information.
    """

    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    # Normalize Unicode characters
    text = unicodedata.normalize("NFC", text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Replace multiple whitespace characters
    # with a single space
    text = re.sub(r"\s+", " ", text)

    # Remove leading and trailing spaces
    text = text.strip()

    return text