import re
import logging

logging.basicConfig(level=logging.INFO)

def clean_text(text: str) -> str:
    """
    Clean and normalize input text by removing extra whitespace.

    Args:
        text (str): Raw input text.

    Returns:
        str: Cleaned text.
    """
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text

def split_into_sentences(text: str):
    """
    Split a text into individual sentences based on punctuation.

    Args:
        text (str): Input text.

    Returns:
        list[str]: List of sentences.
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences
