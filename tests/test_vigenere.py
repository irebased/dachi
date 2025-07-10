"""Tests for the Vigenère cipher implementation."""

import pytest

from dachi.core.alphabet import Alphabet
from dachi.ciphers.vigenere import VigenereCipher


class TestVigenereCipher:
    """Test cases for the Vigenère cipher."""

    def test_standard_vigenere_encryption(self):
        """Test standard Vigenère encryption."""
        cipher = VigenereCipher()
        result = cipher.encrypt("HELLO", "KEY")
        assert result.success
        assert str(result) == "RIJVS"

    def test_standard_vigenere_decryption(self):
        """Test standard Vigenère decryption."""
        cipher = VigenereCipher()
        result = cipher.decrypt("RIJVS", "KEY")
        assert result.success
        assert str(result) == "HELLO"

    def test_autokey_encryption(self):
        """Test autokey Vigenère encryption."""
        cipher = VigenereCipher(autokey=True)
        result = cipher.encrypt("HELLO", "KEY")
        assert result.success
        # Autokey result will be different from standard
        assert str(result) != "RIJVS"

    def test_autokey_decryption(self):
        """Test autokey Vigenère decryption."""
        cipher = VigenereCipher(autokey=True)
        # First encrypt
        encrypted = cipher.encrypt("HELLO", "KEY")
        assert encrypted.success

        # Then decrypt
        decrypted = cipher.decrypt(str(encrypted), "KEY")
        assert decrypted.success
        assert str(decrypted) == "HELLO"

    def test_custom_alphabet(self):
        """Test Vigenère with custom alphabet."""
        alphabet = Alphabet(characters="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        cipher = VigenereCipher(alphabet=alphabet)
        result = cipher.encrypt("HELLO", "KEY")
        assert result.success

    def test_spaces_preservation(self):
        """Test that spaces are preserved during encryption/decryption."""
        cipher = VigenereCipher()
        text = "HELLO WORLD"
        result = cipher.encrypt(text, "KEY")
        assert result.success
        assert " " in str(result)

        decrypted = cipher.decrypt(str(result), "KEY")
        assert decrypted.success
        assert str(decrypted) == text

    def test_empty_text_validation(self):
        """Test validation of empty text."""
        cipher = VigenereCipher()
        result = cipher.encrypt("", "KEY")
        assert not result.success
        assert "Text cannot be empty" in result.error_message

    def test_empty_key_validation(self):
        """Test validation of empty key."""
        cipher = VigenereCipher()
        result = cipher.encrypt("HELLO", "")
        assert not result.success
        assert "Key cannot be empty" in result.error_message

    def test_invalid_key_characters(self):
        """Test validation of key with invalid characters."""
        cipher = VigenereCipher()
        result = cipher.encrypt("HELLO", "KEY123")
        assert not result.success
        assert "Key contains characters not in alphabet" in result.error_message

    def test_invalid_text_characters(self):
        """Test validation of text with invalid characters."""
        cipher = VigenereCipher()
        result = cipher.encrypt("HELLO123", "KEY")
        assert not result.success
        assert "Text contains characters not in alphabet" in result.error_message

    def test_round_trip_encryption(self):
        """Test that encryption followed by decryption returns original text."""
        cipher = VigenereCipher()
        original_text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        key = "SECRET"

        encrypted = cipher.encrypt(original_text, key)
        assert encrypted.success

        decrypted = cipher.decrypt(str(encrypted), key)
        assert decrypted.success
        assert str(decrypted) == original_text

    def test_autokey_round_trip(self):
        """Test autokey round trip encryption/decryption."""
        cipher = VigenereCipher(autokey=True)
        original_text = "HELLO WORLD"
        key = "SECRET"

        encrypted = cipher.encrypt(original_text, key)
        assert encrypted.success

        decrypted = cipher.decrypt(str(encrypted), key)
        assert decrypted.success
        assert str(decrypted) == original_text

    def test_case_sensitive_alphabet(self):
        """Test with case-sensitive alphabet."""
        alphabet = Alphabet(characters="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        cipher = VigenereCipher(alphabet=alphabet)
        result = cipher.encrypt("Hello", "Key")
        assert result.success

    def test_case_insensitive_alphabet(self):
        """Test with case-insensitive alphabet."""
        alphabet = Alphabet(characters="ABCDEFGHIJKLMNOPQRSTUVWXYZ", case_sensitive=False)
        cipher = VigenereCipher(alphabet=alphabet)
        result = cipher.encrypt("hello", "key")
        assert result.success

    def test_supports_autokey(self):
        """Test that Vigenère cipher supports autokey."""
        cipher = VigenereCipher()
        assert cipher.supports_autokey() is True

    def test_create_standard(self):
        """Test creating standard Vigenère cipher."""
        cipher = VigenereCipher.create_standard()
        assert cipher.autokey is False

    def test_create_autokey(self):
        """Test creating autokey Vigenère cipher."""
        cipher = VigenereCipher.create_autokey()
        assert cipher.autokey is True

    def test_character_transformation(self):
        """Test individual character transformation."""
        cipher = VigenereCipher()
        # A (0) + K (10) = K (10)
        assert cipher.transform_character("A", "K") == "K"
        # B (1) + E (4) = F (5)
        assert cipher.transform_character("B", "E") == "F"

    def test_character_reverse_transformation(self):
        """Test individual character reverse transformation."""
        cipher = VigenereCipher()
        # K (10) - K (10) = A (0)
        assert cipher.reverse_transform_character("K", "K") == "A"
        # F (5) - E (4) = B (1)
        assert cipher.reverse_transform_character("F", "E") == "B"

    def test_long_text_encryption(self):
        """Test encryption of longer text."""
        cipher = VigenereCipher()
        long_text = "THIS IS A LONGER TEXT THAT SHOULD BE ENCRYPTED PROPERLY"
        key = "VERYLONGKEY"
        result = cipher.encrypt(long_text, key)
        assert result.success
        assert len(str(result)) == len(long_text)

    def test_special_characters_in_alphabet(self):
        """Test with alphabet containing special characters."""
        alphabet = Alphabet(characters="ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()")
        cipher = VigenereCipher(alphabet=alphabet)
        result = cipher.encrypt("HELLO", "KEY")
        assert result.success

    @pytest.mark.parametrize("text,key,expected", [
        ("A", "A", "A"),
        ("A", "B", "B"),
        ("B", "A", "B"),
        ("Z", "A", "Z"),
        ("A", "Z", "Z"),
    ])
    def test_edge_cases(self, text, key, expected):
        """Test edge cases for Vigenère cipher."""
        cipher = VigenereCipher()
        result = cipher.encrypt(text, key)
        assert result.success
        assert str(result) == expected