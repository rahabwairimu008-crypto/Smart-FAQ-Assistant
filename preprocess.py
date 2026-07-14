"""
preprocess.py
Cleans and tokenizes raw student queries before grammar parsing.
"""

import re


def clean_text(text: str) -> str:
    """Lowercase, strip extra whitespace, normalize common variants."""
    text = text.strip().lower()

    # Normalize common abbreviations / variants seen in the 70 queries
    replacements = {
        "cod": "chairperson of department",
        "cat": "continuous assessment test",
        "b.sc": "bachelor of science",
        "bsc": "bachelor of science",
        "e.g.": "for example",
    }
    for old, new in replacements.items():
        text = re.sub(rf"\b{re.escape(old)}\b", new, text)

    return text


def tokenize(text: str) -> list:
    """
    Turn a cleaned sentence into a list of tokens the grammar can consume.
    The trailing '?' is kept as its own QMARK token since the grammar
    expects it as a terminal. If the person didn't type a '?' (very
    common when typing quickly), one is appended automatically so the
    grammar still recognizes the sentence as a complete question.
    """
    text = clean_text(text)

    # Separate punctuation (esp. '?') from words
    text = re.sub(r"([?.,])", r" \1 ", text)
    tokens = text.split()

    if not tokens or tokens[-1] != "?":
        tokens.append("?")

    return tokens


if __name__ == "__main__":
    samples = [
        "How do I register for my courses?",
        "Can I defer my studies?",
        "What happens if I miss an end-of-semester examination?",
    ]
    for s in samples:
        print(s, "->", tokenize(s))