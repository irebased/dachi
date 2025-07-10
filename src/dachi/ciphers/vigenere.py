"""Vigenère cipher implementation with autokey support."""

from typing import Optional

from ..core.alphabet import Alphabet
from ..core.cipher import StreamCipher, CipherResult, BaseCipherResult
from ..core.key import Key


class VigenereCipher(StreamCipher):
    """Vigenère cipher implementation with support for autokey mode.

    The Vigenère cipher is a method of encrypting alphabetic text by using
    a simple form of polyalphabetic substitution. It was first described
    by Giovan Battista Bellaso in 1553, but the scheme is now known as
    the Vigenère cipher after Blaise de Vigenère.

    This implementation supports:
    - Custom alphabets
    - Autokey mode (key + plaintext)
    - Standard mode (repeating key)
    """

    def __init__(self, alphabet: Optional[Alphabet] = None, autokey: bool = False):
        """Initialize the Vigenère cipher.

        Args:
            alphabet: The alphabet to use (defaults to standard English)
            autokey: Whether to use autokey mode
        """
        if alphabet is None:
            alphabet = Alphabet.standard_english()

        super().__init__(alphabet)
        self.autokey = autokey

    def transform_character(self, char: str, key_char: str) -> str:
        """Transform a character using Vigenère encryption.

        Args:
            char: The character to encrypt
            key_char: The key character

        Returns:
            The encrypted character
        """
        char_idx = self.alphabet.get_char_index(char)
        key_idx = self.alphabet.get_char_index(key_char)

        if char_idx is None or key_idx is None:
            raise ValueError(f"Invalid character or key character: {char}, {key_char}")

        # Vigenère encryption: (char_idx + key_idx) mod alphabet_size
        encrypted_idx = (char_idx + key_idx) % len(self.alphabet)
        return self.alphabet.get_char_at_index(encrypted_idx) or char

    def reverse_transform_character(self, char: str, key_char: str) -> str:
        """Reverse transform a character using Vigenère decryption.

        Args:
            char: The character to decrypt
            key_char: The key character

        Returns:
            The decrypted character
        """
        char_idx = self.alphabet.get_char_index(char)
        key_idx = self.alphabet.get_char_index(key_char)

        if char_idx is None or key_idx is None:
            raise ValueError(f"Invalid character or key character: {char}, {key_char}")

        # Vigenère decryption: (char_idx - key_idx) mod alphabet_size
        decrypted_idx = (char_idx - key_idx) % len(self.alphabet)
        return self.alphabet.get_char_at_index(decrypted_idx) or char

    def encrypt(self, plaintext: str, key: str) -> CipherResult:
        """Encrypt plaintext using Vigenère cipher.

        Args:
            plaintext: The text to encrypt
            key: The encryption key

        Returns:
            CipherResult containing the encrypted text or error information
        """
        error = self.validate_input(plaintext, key)
        if error:
            return BaseCipherResult.error_result(error)

        try:
            key_obj = Key.from_string(key, self.alphabet)
            processed_text = self.preprocess_text(plaintext)

            # For autokey, we need the plaintext to generate the key stream
            if self.autokey:
                nonspace_plaintext = ''.join(c for c in processed_text if not c.isspace())
                key_stream = key_obj.get_key_stream(
                    len(nonspace_plaintext),
                    autokey=True,
                    plaintext=nonspace_plaintext
                )
            else:
                key_stream = key_obj.get_key_stream(len(processed_text))

            result_chars = []
            key_idx = 0
            for char in processed_text:
                if char.isspace():
                    result_chars.append(char)
                else:
                    key_char = self.alphabet.get_char_at_index(key_stream[key_idx])
                    if key_char is None:
                        return BaseCipherResult.error_result(f"Invalid key character at position {key_idx}")
                    transformed = self.transform_character(char, key_char)
                    result_chars.append(transformed)
                    key_idx += 1

            result = "".join(result_chars)
            return BaseCipherResult.success_result(self.postprocess_text(result))

        except Exception as e:
            return BaseCipherResult.error_result(f"Encryption failed: {e}")

    def decrypt(self, ciphertext: str, key: str) -> CipherResult:
        """Decrypt ciphertext using Vigenère cipher.

        Args:
            ciphertext: The text to decrypt
            key: The decryption key

        Returns:
            CipherResult containing the decrypted text or error information
        """
        error = self.validate_input(ciphertext, key)
        if error:
            return BaseCipherResult.error_result(error)

        try:
            key_obj = Key.from_string(key, self.alphabet)
            processed_text = self.preprocess_text(ciphertext)

            # For autokey decryption, we need to reconstruct the key stream
            # This is more complex as we need to decrypt progressively
            if self.autokey:
                return self._decrypt_autokey(processed_text, key_obj)
            else:
                key_stream = key_obj.get_key_stream(len(processed_text))

                result_chars = []
                key_idx = 0
                for char in processed_text:
                    if char.isspace():
                        result_chars.append(char)
                    else:
                        key_char = self.alphabet.get_char_at_index(key_stream[key_idx])
                        if key_char is None:
                            return BaseCipherResult.error_result(f"Invalid key character at position {key_idx}")

                        transformed = self.reverse_transform_character(char, key_char)
                        result_chars.append(transformed)
                        key_idx += 1

                result = "".join(result_chars)
                return BaseCipherResult.success_result(self.postprocess_text(result))

        except Exception as e:
            return BaseCipherResult.error_result(f"Decryption failed: {e}")

    def _decrypt_autokey(self, ciphertext: str, key_obj: Key) -> CipherResult:
        """Decrypt ciphertext using autokey mode.

        Args:
            ciphertext: The text to decrypt
            key_obj: The key object

        Returns:
            CipherResult containing the decrypted text or error information
        """
        try:
            result_chars = []
            key_chars = list(key_obj.normalize())
            key_length = len(key_chars)
            nonspace_decrypted = []
            key_idx = 0

            for char in ciphertext:
                if char.isspace():
                    result_chars.append(char)
                else:
                    if key_idx < key_length:
                        key_char = key_chars[key_idx]
                    else:
                        key_char = nonspace_decrypted[key_idx - key_length]
                    decrypted_char = self.reverse_transform_character(char, key_char)
                    result_chars.append(decrypted_char)
                    nonspace_decrypted.append(decrypted_char)
                    key_idx += 1

            result = "".join(result_chars)
            return BaseCipherResult.success_result(self.postprocess_text(result))

        except Exception as e:
            return BaseCipherResult.error_result(f"Autokey decryption failed: {e}")

    def supports_autokey(self) -> bool:
        """Check if this cipher supports autokey mode.

        Returns:
            True (Vigenère cipher supports autokey)
        """
        return True

    @classmethod
    def create_standard(cls, alphabet: Optional[Alphabet] = None) -> "VigenereCipher":
        """Create a standard Vigenère cipher (no autokey).

        Args:
            alphabet: The alphabet to use

        Returns:
            A Vigenère cipher instance
        """
        return cls(alphabet=alphabet, autokey=False)

    @classmethod
    def create_autokey(cls, alphabet: Optional[Alphabet] = None) -> "VigenereCipher":
        """Create an autokey Vigenère cipher.

        Args:
            alphabet: The alphabet to use

        Returns:
            A Vigenère cipher instance with autokey enabled
        """
        return cls(alphabet=alphabet, autokey=True)