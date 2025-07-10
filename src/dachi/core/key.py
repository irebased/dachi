"""Key management for cryptographic operations."""

from typing import List, Optional
from pydantic import BaseModel, Field, validator

from .alphabet import Alphabet


class Key(BaseModel):
    """Represents a cryptographic key with validation and processing capabilities."""

    value: str = Field(..., description="The key value")
    alphabet: Alphabet = Field(..., description="The alphabet this key operates on")

    class Config:
        frozen = True

    @validator("value")
    def validate_key(cls, v: str) -> str:
        """Validate that the key is not empty."""
        if not v:
            raise ValueError("Key cannot be empty")
        return v

    def __len__(self) -> int:
        """Return the length of the key."""
        return len(self.value)

    def normalize(self) -> str:
        """Normalize the key according to the alphabet's case sensitivity."""
        return self.alphabet.normalize(self.value)

    def validate(self) -> bool:
        """Check if all characters in the key are in the alphabet."""
        normalized_key = self.normalize()
        return all(char in self.alphabet for char in normalized_key)

    def get_key_stream(self, length: int, autokey: bool = False, plaintext: str = "") -> List[int]:
        """Generate a key stream for encryption/decryption.

        Args:
            length: The length of the key stream needed
            autokey: Whether to use autokey mode
            plaintext: The plaintext (needed for autokey mode)

        Returns:
            List of key indices
        """
        if not self.validate():
            raise ValueError("Key contains characters not in the alphabet")

        normalized_key = self.normalize()
        key_indices = [self.alphabet.get_char_index(char) for char in normalized_key]

        if not autokey:
            # Standard Vigenère: repeat the key
            return [key_indices[i % len(key_indices)] for i in range(length)]
        else:
            # Autokey: key + plaintext
            if not plaintext:
                raise ValueError("Plaintext required for autokey mode")

            normalized_plaintext = self.alphabet.normalize(plaintext)
            plaintext_indices = [
                self.alphabet.get_char_index(char)
                for char in normalized_plaintext
                if char in self.alphabet
            ]

            # Combine key and plaintext indices
            combined = key_indices + plaintext_indices
            return combined[:length]

    def get_key_indices(self) -> List[int]:
        """Get the indices of key characters in the alphabet."""
        normalized_key = self.normalize()
        indices = []
        for char in normalized_key:
            idx = self.alphabet.get_char_index(char)
            if idx is not None:
                indices.append(idx)
        return indices

    @classmethod
    def from_string(cls, key_str: str, alphabet: Alphabet) -> "Key":
        """Create a key from a string and alphabet."""
        return cls(value=key_str, alphabet=alphabet)

    def __str__(self) -> str:
        """String representation of the key."""
        return self.value