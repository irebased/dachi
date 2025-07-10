"""Alphabet management for cryptographic operations."""

from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field, validator


class Alphabet(BaseModel):
    """Represents a custom alphabet for cryptographic operations.

    This class provides a robust foundation for managing alphabets with
    strong validation and efficient character mapping.
    """

    characters: str = Field(..., description="The characters in the alphabet")
    case_sensitive: bool = Field(default=True, description="Whether the alphabet is case sensitive")

    class Config:
        frozen = True

    @validator("characters")
    def validate_characters(cls, v: str) -> str:
        """Validate that the alphabet contains unique characters."""
        if not v:
            raise ValueError("Alphabet cannot be empty")

        if len(v) != len(set(v)):
            raise ValueError("Alphabet must contain unique characters")

        return v

    def __len__(self) -> int:
        """Return the length of the alphabet."""
        return len(self.characters)

    def __contains__(self, item: str) -> bool:
        """Check if a character is in the alphabet."""
        if not self.case_sensitive:
            return item.upper() in self.characters.upper()
        return item in self.characters

    def normalize(self, text: str) -> str:
        """Normalize text according to alphabet case sensitivity."""
        if not self.case_sensitive:
            return text.upper()
        return text

    def get_char_index(self, char: str) -> Optional[int]:
        """Get the index of a character in the alphabet."""
        normalized_char = self.normalize(char)
        try:
            return self.characters.index(normalized_char)
        except ValueError:
            return None

    def get_char_at_index(self, index: int) -> Optional[str]:
        """Get the character at a specific index."""
        if 0 <= index < len(self.characters):
            return self.characters[index]
        return None

    def get_mapping(self) -> Dict[str, int]:
        """Get a mapping of characters to their indices."""
        return {char: idx for idx, char in enumerate(self.characters)}

    def get_reverse_mapping(self) -> Dict[int, str]:
        """Get a mapping of indices to characters."""
        return {idx: char for idx, char in enumerate(self.characters)}

    def filter_text(self, text: str, preserve_spaces: bool = True) -> str:
        """Filter text to only include characters in the alphabet."""
        if preserve_spaces:
            # Filter characters but preserve spaces
            result = ""
            kept_indices = []
            for idx, char in enumerate(text):
                if char in self or char.isspace():
                    result += char
                    if char in self:
                        kept_indices.append(idx)
            # Only append a single trailing space if the last kept character was followed by a space
            if kept_indices:
                last_idx = kept_indices[-1]
                # Remove all spaces after the last kept character
                result = result[:len(result) - (len(result) - last_idx - 1)]
                # If the original input had a space immediately after the last kept character, append one space
                if last_idx + 1 < len(text) and text[last_idx + 1].isspace():
                    result += ' '
            return result
        return "".join(char for char in text if char in self)

    def validate_text(self, text: str) -> bool:
        """Check if all characters in text are in the alphabet."""
        return all(char in self or char.isspace() for char in text)

    @classmethod
    def standard_english(cls) -> "Alphabet":
        """Create a standard English alphabet (A-Z)."""
        return cls(characters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    @classmethod
    def extended_english(cls) -> "Alphabet":
        """Create an extended English alphabet (A-Z, a-z, 0-9, punctuation)."""
        return cls(
            characters="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?",
            case_sensitive=True
        )

    @classmethod
    def case_insensitive_english(cls) -> "Alphabet":
        """Create a case-insensitive English alphabet."""
        return cls(
            characters="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            case_sensitive=False
        )