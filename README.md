# Dachi - Cryptographic CLI Tool

A powerful command-line tool for cryptographic operations, featuring a highly extensible architecture with strong abstraction layers.

## Features

- **Vigenère Cipher**: Classic and autokey variants with custom alphabets
- **Extensible Architecture**: Easy to add new ciphers and cryptographic operations
- **Rich CLI Interface**: Beautiful terminal output with progress indicators
- **Type Safety**: Full type hints and validation with Pydantic
- **Comprehensive Testing**: Unit and integration tests with high coverage

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/dachi.git
cd dachi

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### Development Setup

```bash
# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Format code
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/
```

## Usage

### Vigenère Cipher

#### Basic Usage

```bash
# Encrypt with standard alphabet
dachi vigenere encrypt --key "SECRET" --text "HELLO WORLD"

# Decrypt with standard alphabet
dachi vigenere decrypt --key "SECRET" --text "ZINCS VGXCS"

# Use custom alphabet
dachi vigenere encrypt --key "KEY" --text "HELLO" --alphabet "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
```

#### Autokey Mode

```bash
# Encrypt with autokey (key + plaintext)
dachi vigenere encrypt --key "SECRET" --text "HELLO WORLD" --autokey

# Decrypt with autokey
dachi vigenere decrypt --key "SECRET" --text "ZINCS VGXCS" --autokey
```

#### Advanced Options

```bash
# Use a custom alphabet with special characters
dachi vigenere encrypt --key "KEY" --text "Hello, World!" --alphabet "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"

# Read from file
dachi vigenere encrypt --key "SECRET" --input-file message.txt --output-file encrypted.txt

# Interactive mode
dachi vigenere encrypt --key "SECRET" --interactive
```

### Programmatic Usage

```python
from dachi.ciphers.vigenere import VigenereCipher
from dachi.core.alphabet import Alphabet

# Create cipher with custom alphabet
alphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
cipher = VigenereCipher(alphabet=alphabet)

# Encrypt
encrypted = cipher.encrypt("HELLO WORLD", "SECRET")
print(encrypted)  # Output: ZINCS VGXCS

# Decrypt
decrypted = cipher.decrypt("ZINCS VGXCS", "SECRET")
print(decrypted)  # Output: HELLO WORLD

# Autokey mode
cipher_autokey = VigenereCipher(alphabet=alphabet, autokey=True)
encrypted_ak = cipher_autokey.encrypt("HELLO WORLD", "SECRET")
```

## Architecture

The project is built with strong abstraction layers for optimal extensibility:

### Core Components

- **`dachi.core.alphabet`**: Alphabet management and validation
- **`dachi.core.cipher`**: Abstract base classes for all ciphers
- **`dachi.core.key`**: Key management and validation
- **`dachi.ciphers.vigenere`**: Vigenère cipher implementation
- **`dachi.cli`**: Command-line interface using Click
- **`dachi.utils`**: Utility functions and helpers

### Adding New Ciphers

To add a new cipher, inherit from the base cipher class:

```python
from dachi.core.cipher import Cipher
from dachi.core.alphabet import Alphabet

class MyCipher(Cipher):
    def __init__(self, alphabet: Alphabet):
        super().__init__(alphabet)

    def encrypt(self, plaintext: str, key: str) -> str:
        # Implementation here
        pass

    def decrypt(self, ciphertext: str, key: str) -> str:
        # Implementation here
        pass
```

## Development

### Project Structure

```
dachi/
├── src/
│   └── dachi/
│       ├── __init__.py
│       ├── cli.py              # CLI entry point
│       ├── core/               # Core abstractions
│       │   ├── __init__.py
│       │   ├── alphabet.py     # Alphabet management
│       │   ├── cipher.py       # Base cipher classes
│       │   └── key.py          # Key management
│       ├── ciphers/            # Cipher implementations
│       │   ├── __init__.py
│       │   └── vigenere.py     # Vigenère cipher
│       └── utils/              # Utilities
│           ├── __init__.py
│           └── text.py         # Text processing
├── tests/                      # Test suite
├── pyproject.toml             # Project configuration
├── README.md                  # This file
└── .pre-commit-config.yaml    # Pre-commit hooks
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=dachi --cov-report=html

# Run specific test file
pytest tests/test_vigenere.py

# Run with verbose output
pytest -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.