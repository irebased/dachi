"""Text processing utilities for cryptographic operations."""

import re
from typing import Optional


def normalize_text(text: str, remove_spaces: bool = False) -> str:
    """Normalize text for cryptographic operations.

    Args:
        text: The text to normalize
        remove_spaces: Whether to remove spaces

    Returns:
        Normalized text
    """
    if remove_spaces:
        return re.sub(r'\s+', '', text.upper())
    return text.strip()


def validate_input(text: str, max_length: Optional[int] = None) -> Optional[str]:
    """Validate input text.

    Args:
        text: The text to validate
        max_length: Maximum allowed length

    Returns:
        Error message if validation fails, None if successful
    """
    if not text:
        return "Text cannot be empty"

    if max_length and len(text) > max_length:
        return f"Text exceeds maximum length of {max_length} characters"

    return None


def chunk_text(text: str, chunk_size: int) -> list[str]:
    """Split text into chunks of specified size.

    Args:
        text: The text to chunk
        chunk_size: Size of each chunk

    Returns:
        List of text chunks
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def format_output(text: str, chunk_size: int = 5, separator: str = " ") -> str:
    """Format output text with chunking for readability.

    Args:
        text: The text to format
        chunk_size: Size of each chunk
        separator: Separator between chunks

    Returns:
        Formatted text
    """
    chunks = chunk_text(text, chunk_size)
    return separator.join(chunks)


def remove_non_alphanumeric(text: str, preserve_spaces: bool = True) -> str:
    """Remove non-alphanumeric characters from text.

    Args:
        text: The text to process
        preserve_spaces: Whether to preserve spaces

    Returns:
        Processed text
    """
    if preserve_spaces:
        return re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return re.sub(r'[^a-zA-Z0-9]', '', text)