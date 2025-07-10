"""Alphabet generation utilities for creating keyed alphabets from word lists."""

import re
from pathlib import Path
from typing import List, Set

from ..core.alphabet import Alphabet


class AlphabetGenerator:
    """Generates keyed alphabets from word lists.

    This class provides functionality to create custom alphabets where
    specific words or phrases appear at the beginning without repeating letters.
    """

    @staticmethod
    def parse_word_list(file_path: str) -> List[str]:
        """Parse a text file containing words/phrases.

        Supports comma-separated, space-separated, or newline-separated formats.

        Args:
            file_path: Path to the text file containing words/phrases

        Returns:
            List of words/phrases from the file

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is empty or contains no valid words
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
                words = [word.strip() for word in content.split(sep) if word.strip()]
                if words:
                    return words

        # If no separators found, treat the entire content as a single word
        return [content]

    @staticmethod
    def generate_keyed_alphabet(words: List[str], base_alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> str:
        """Generate a keyed alphabet from a list of words.

        Args:
            words: List of words/phrases to use as keys
            base_alphabet: Base alphabet to use for remaining characters

        Returns:
            Generated keyed alphabet string

        Raises:
            ValueError: If no valid characters found in words
        """
        if not words:
            raise ValueError("No words provided")

        # Normalize words to uppercase and remove non-alphabetic characters
        normalized_words = []
        for word in words:
            normalized = re.sub(r'[^A-Za-z]', '', word.upper())
            if normalized:
                normalized_words.append(normalized)

        if not normalized_words:
            raise ValueError("No valid alphabetic characters found in words")

        # Build the keyed alphabet
        used_chars: Set[str] = set()
        keyed_alphabet = ""

        # Add characters from words in order, avoiding duplicates
        for word in normalized_words:
            for char in word:
                if char not in used_chars:
                    keyed_alphabet += char
                    used_chars.add(char)

        # Add remaining characters from base alphabet
        for char in base_alphabet:
            if char not in used_chars:
                keyed_alphabet += char
                used_chars.add(char)

        return keyed_alphabet

    @staticmethod
    def create_alphabet_from_file(file_path: str, base_alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> Alphabet:
        """Create an Alphabet object from a word list file.

        Args:
            file_path: Path to the text file containing words/phrases
            base_alphabet: Base alphabet to use for remaining characters

        Returns:
            Alphabet object with the generated keyed alphabet

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is empty or contains no valid words
        """
        words = AlphabetGenerator.parse_word_list(file_path)
        keyed_alphabet = AlphabetGenerator.generate_keyed_alphabet(words, base_alphabet)
        return Alphabet(characters=keyed_alphabet)

    @staticmethod
    def generate_multiple_alphabets(file_path: str, base_alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> List[Alphabet]:
        """Generate multiple alphabets from a word list file.

        Each word/phrase in the file will be used to generate a separate alphabet.

        Args:
            file_path: Path to the text file containing words/phrases
            base_alphabet: Base alphabet to use for remaining characters

        Returns:
            List of Alphabet objects, one for each word/phrase

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is empty or contains no valid words
        """
        words = AlphabetGenerator.parse_word_list(file_path)
        alphabets = []

        for word in words:
            keyed_alphabet = AlphabetGenerator.generate_keyed_alphabet([word], base_alphabet)
            alphabets.append(Alphabet(characters=keyed_alphabet))

        return alphabets