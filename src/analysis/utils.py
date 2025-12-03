import re
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO)

import re
import nltk
from nltk.corpus import stopwords

# Download stopwords if not already downloaded
nltk.download('stopwords')
STOP_WORDS = set(stopwords.words('english'))

def remove_punctuation_and_stopwords(text: str) -> str:
    """
    Remove punctuation and stop words from text.

    Args:
        text (str): Input text.

    Returns:
        str: Cleaned text without punctuation or stop words.
    """
    # Lowercase text
    text = text.lower()
    
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # Remove stop words
    words = text.split()
    words = [word for word in words if word not in STOP_WORDS]
    
    cleaned_text = ' '.join(words)
    return cleaned_text


def clean_text(text: str) -> str:
    """
    Normalize and clean input text.

    - Removes extra whitespace.
    - Trims leading and trailing spaces.

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
    Split text into individual sentences.

    The function uses punctuation (. ! ?) as sentence boundaries.

    Args:
        text (str): Input text.

    Returns:
        List[str]: List of sentence strings.
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def chunk_text(text: str, max_chunk_size=4000):
    """
    Chunk raw text using LangChain's RecursiveCharacterTextSplitter.

    Args:
        text (str): Input text string.
        max_chunk_size (int): Maximum size of each chunk.

    Returns:
        List[str]: List of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_chunk_size,
        chunk_overlap=0
    )

    docs = text_splitter.create_documents([text])
    chunks = [doc.page_content for doc in docs]

    logging.info(f"Generated {len(chunks)} chunks.")
    return chunks
