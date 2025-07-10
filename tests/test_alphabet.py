"""Tests for the Alphabet class."""

import pytest

from dachi.core.alphabet import Alphabet


class TestAlphabet:
    """Test cases for the Alphabet class."""

    def test_standard_english_alphabet(self):
        """Test standard English alphabet creation."""
        alphabet = Alphabet.standard_english()
        assert len(alphabet) == 26
        assert alphabet.characters == "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        assert alphabet.case_sensitive is True

    def test_extended_english_alphabet(self):
        """Test extended English alphabet creation."""
        alphabet = Alphabet.extended_english()
        assert len(alphabet) > 26
        assert "A" in alphabet.characters
        assert "z" in alphabet.characters
        assert "0" in alphabet.characters
        assert "!" in alphabet.characters

    def test_case_insensitive_alphabet(self):
        """Test case-insensitive alphabet creation."""
        alphabet = Alphabet.case_insensitive_english()
        assert alphabet.case_sensitive is False
        assert "A" in alphabet
        assert "a" in alphabet
        assert alphabet.normalize("hello") == "HELLO"

    def test_custom_alphabet(self):
        """Test custom alphabet creation."""
        alphabet = Alphabet(characters="ABC123")
        assert len(alphabet) == 6
        assert alphabet.characters == "ABC123"

    def test_empty_alphabet_validation(self):
        """Test that empty alphabet raises ValueError."""
        with pytest.raises(ValueError, match="Alphabet cannot be empty"):
            Alphabet(characters="")

    def test_duplicate_characters_validation(self):
        """Test that duplicate characters raise ValueError."""
        with pytest.raises(ValueError, match="Alphabet must contain unique characters"):
            Alphabet(characters="AAB")

    def test_character_containment(self):
        """Test character containment checks."""
        alphabet = Alphabet(characters="ABC")
        assert "A" in alphabet
        assert "B" in alphabet
        assert "C" in alphabet
        assert "D" not in alphabet

    def test_case_insensitive_containment(self):
        """Test character containment with case-insensitive alphabet."""
        alphabet = Alphabet(characters="ABC", case_sensitive=False)
        assert "A" in alphabet
        assert "a" in alphabet
        assert "B" in alphabet
        assert "b" in alphabet

    def test_normalize_text(self):
        """Test text normalization."""
        alphabet = Alphabet(characters="ABC", case_sensitive=False)
        assert alphabet.normalize("abc") == "ABC"

        alphabet = Alphabet(characters="ABC", case_sensitive=True)
        assert alphabet.normalize("abc") == "abc"

    def test_get_char_index(self):
        """Test getting character index."""
        alphabet = Alphabet(characters="ABC")
        assert alphabet.get_char_index("A") == 0
        assert alphabet.get_char_index("B") == 1
        assert alphabet.get_char_index("C") == 2
        assert alphabet.get_char_index("D") is None

    def test_get_char_at_index(self):
        """Test getting character at index."""
        alphabet = Alphabet(characters="ABC")
        assert alphabet.get_char_at_index(0) == "A"
        assert alphabet.get_char_at_index(1) == "B"
        assert alphabet.get_char_at_index(2) == "C"
        assert alphabet.get_char_at_index(3) is None
        assert alphabet.get_char_at_index(-1) is None

    def test_get_mapping(self):
        """Test getting character to index mapping."""
        alphabet = Alphabet(characters="ABC")
        mapping = alphabet.get_mapping()
        expected = {"A": 0, "B": 1, "C": 2}
        assert mapping == expected

    def test_get_reverse_mapping(self):
        """Test getting index to character mapping."""
        alphabet = Alphabet(characters="ABC")
        reverse_mapping = alphabet.get_reverse_mapping()
        expected = {0: "A", 1: "B", 2: "C"}
        assert reverse_mapping == expected

    def test_filter_text(self):
        """Test text filtering."""
        alphabet = Alphabet(characters="ABC")
        text = "A B C D E"
        filtered = alphabet.filter_text(text, preserve_spaces=True)
        assert filtered == "A B C "

        filtered = alphabet.filter_text(text, preserve_spaces=False)
        assert filtered == "ABC"

    def test_validate_text(self):
        """Test text validation."""
        alphabet = Alphabet(characters="ABC")
        assert alphabet.validate_text("A B C") is True
        assert alphabet.validate_text("A B C D") is False
        assert alphabet.validate_text("") is True

    def test_frozen_config(self):
        """Test that alphabet is immutable."""
        alphabet = Alphabet(characters="ABC")
        with pytest.raises(Exception):
            alphabet.characters = "XYZ"