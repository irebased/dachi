"""Abstract base classes for cryptographic ciphers."""

from abc import ABC, abstractmethod
from typing import Optional, Protocol

from .alphabet import Alphabet
from .key import Key


class CipherResult(Protocol):
    """Protocol for cipher operation results."""

    def __str__(self) -> str:
        """Return the result as a string."""
        ...

    @property
    def success(self) -> bool:
        """Whether the operation was successful."""
        ...

    @property
    def error_message(self) -> Optional[str]:
        """Error message if the operation failed."""
        ...


class BaseCipherResult:
    """Base implementation of CipherResult."""

    def __init__(self, result: str, success: bool = True, error_message: Optional[str] = None):
        self._result = result
        self._success = success
        self._error_message = error_message

    def __str__(self) -> str:
        return self._result

    @property
    def success(self) -> bool:
        return self._success

    @property
    def error_message(self) -> Optional[str]:
        return self._error_message

    @classmethod
    def success_result(cls, result: str) -> "BaseCipherResult":
        """Create a successful result."""
        return cls(result=result, success=True)

    @classmethod
    def error_result(cls, error_message: str) -> "BaseCipherResult":
        """Create an error result."""
        return cls(result="", success=False, error_message=error_message)


class Cipher(ABC):
    """Abstract base class for all cryptographic ciphers.

    This class provides a strong foundation for implementing various
    cryptographic algorithms with consistent interfaces and validation.
    """

    def __init__(self, alphabet: Alphabet):
        """Initialize the cipher with an alphabet.

        Args:
            alphabet: The alphabet to use for this cipher
        """
        self.alphabet = alphabet

    @abstractmethod
    def encrypt(self, plaintext: str, key: str) -> CipherResult:
        """Encrypt plaintext using the given key.

        Args:
            plaintext: The text to encrypt
            key: The encryption key

        Returns:
            CipherResult containing the encrypted text or error information
        """
        pass

    @abstractmethod
    def decrypt(self, ciphertext: str, key: str) -> CipherResult:
        """Decrypt ciphertext using the given key.

        Args:
            ciphertext: The text to decrypt
            key: The decryption key

        Returns:
            CipherResult containing the decrypted text or error information
        """
        pass

    def validate_input(self, text: str, key: str) -> Optional[str]:
        """Validate input text and key.

        Args:
            text: The text to validate
            key: The key to validate

        Returns:
            Error message if validation fails, None if successful
        """
        if not text:
            return "Text cannot be empty"

        if not key:
            return "Key cannot be empty"

        # Create key object for validation
        try:
            key_obj = Key.from_string(key, self.alphabet)
            if not key_obj.validate():
                return f"Key contains characters not in alphabet: {key}"
        except ValueError as e:
            return f"Invalid key: {e}"

        # Preprocess text for validation (convert to uppercase and filter)
        processed_text = self.preprocess_text(text)

        # Validate processed text contains only alphabet characters or spaces
        if not self.alphabet.validate_text(processed_text):
            return f"Text contains characters not in alphabet after processing: {text}"

        return None

    def preprocess_text(self, text: str) -> str:
        """Preprocess text for cipher operations.

        Args:
            text: The text to preprocess

        Returns:
            Preprocessed text
        """
        # Convert to uppercase before filtering
        uppercase_text = text.upper()
        return self.alphabet.filter_text(uppercase_text, preserve_spaces=True)

    def postprocess_text(self, text: str) -> str:
        """Postprocess text after cipher operations.

        Args:
            text: The text to postprocess

        Returns:
            Postprocessed text
        """
        return text

    def get_alphabet_size(self) -> int:
        """Get the size of the alphabet."""
        return len(self.alphabet)

    def supports_autokey(self) -> bool:
        """Check if this cipher supports autokey mode.

        Returns:
            True if autokey is supported, False otherwise
        """
        return False


class StreamCipher(Cipher):
    """Abstract base class for stream ciphers.

    Stream ciphers operate on individual characters and can be
    easily extended for various algorithms.
    """

    def __init__(self, alphabet: Alphabet):
        super().__init__(alphabet)

    @abstractmethod
    def transform_character(self, char: str, key_char: str) -> str:
        """Transform a single character using a key character.

        Args:
            char: The character to transform
            key_char: The key character to use

        Returns:
            The transformed character
        """
        pass

    def encrypt(self, plaintext: str, key: str) -> CipherResult:
        """Encrypt plaintext using stream cipher approach."""
        error = self.validate_input(plaintext, key)
        if error:
            return BaseCipherResult.error_result(error)

        try:
            key_obj = Key.from_string(key, self.alphabet)
            processed_text = self.preprocess_text(plaintext)

            result_chars = []
            key_stream = key_obj.get_key_stream(len(processed_text))

            for i, char in enumerate(processed_text):
                if char.isspace():
                    result_chars.append(char)
                else:
                    key_char = self.alphabet.get_char_at_index(key_stream[i])
                    if key_char is None:
                        return BaseCipherResult.error_result(f"Invalid key character at position {i}")

                    transformed = self.transform_character(char, key_char)
                    result_chars.append(transformed)

            result = "".join(result_chars)
            return BaseCipherResult.success_result(self.postprocess_text(result))

        except Exception as e:
            return BaseCipherResult.error_result(f"Encryption failed: {e}")

    def decrypt(self, ciphertext: str, key: str) -> CipherResult:
        """Decrypt ciphertext using stream cipher approach."""
        error = self.validate_input(ciphertext, key)
        if error:
            return BaseCipherResult.error_result(error)

        try:
            key_obj = Key.from_string(key, self.alphabet)
            processed_text = self.preprocess_text(ciphertext)

            result_chars = []
            key_stream = key_obj.get_key_stream(len(processed_text))

            for i, char in enumerate(processed_text):
                if char.isspace():
                    result_chars.append(char)
                else:
                    key_char = self.alphabet.get_char_at_index(key_stream[i])
                    if key_char is None:
                        return BaseCipherResult.error_result(f"Invalid key character at position {i}")

                    transformed = self.reverse_transform_character(char, key_char)
                    result_chars.append(transformed)

            result = "".join(result_chars)
            return BaseCipherResult.success_result(self.postprocess_text(result))

        except Exception as e:
            return BaseCipherResult.error_result(f"Decryption failed: {e}")

    @abstractmethod
    def reverse_transform_character(self, char: str, key_char: str) -> str:
        """Reverse transform a single character using a key character.

        Args:
            char: The character to reverse transform
            key_char: The key character to use

        Returns:
            The reverse transformed character
        """
        pass