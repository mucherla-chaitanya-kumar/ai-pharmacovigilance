import re

def clean_text(text: str) -> str:
    """
    Cleans and normalizes input text before running NLP models.
    """
    text = re.sub(r'\s+', ' ', text)  # remove extra spaces
    text = re.sub(r'\n+', ' ', text)  # remove newlines
    text = re.sub(r'\[[0-9]*\]', '', text)  # remove reference numbers
    text = text.strip()
    return text
