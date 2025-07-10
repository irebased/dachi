"""Key generation utilities for reading keys from word/phrase lists."""

from pathlib import Path
from typing import List

def parse_key_list(file_path: str) -> List[str]:
    """Parse a text file containing keys (words/phrases).

    Supports comma-separated, space-separated, or newline-separated formats.
    Trims whitespace and removes duplicates, preserving order.

    Args:
        file_path: Path to the text file containing keys

    Returns:
        List of unique keys (strings) from the file

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file is empty or contains no valid keys
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    if not content:
        raise ValueError("File is empty")

    # Try different separators in order of preference
    separators = [',', '\n', ' ']
    for sep in separators:
        if sep in content:
            keys = [key.strip() for key in content.split(sep) if key.strip()]
            # Remove duplicates, preserve order
            seen = set()
            unique_keys = []
            for key in keys:
                if key not in seen:
                    unique_keys.append(key)
                    seen.add(key)
            if unique_keys:
                return unique_keys
    # If no separators found, treat the entire content as a single key
    return [content]