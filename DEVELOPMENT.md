# Development Guide

This guide covers setting up the development environment, running tests, and using the CLI for the Dachi cryptographic tool.

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- git

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/dachi.git
   cd dachi
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

### Using Makefile (Recommended)

The project includes a Makefile with common development commands:

```bash
# Show all available commands
make help

# Install in development mode
make install-dev

# Run all checks (lint, format, type-check, test)
make check-all

# Run tests with coverage
make test-cov

# Format code
make format

# Clean build artifacts
make clean
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=dachi --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_vigenere.py

# Run specific test function
pytest tests/test_vigenere.py::TestVigenereCipher::test_standard_vigenere_encryption

# Run tests with markers
pytest -m "not slow"
```

### Test Structure

- `tests/test_alphabet.py` - Tests for the Alphabet class
- `tests/test_vigenere.py` - Tests for the Vigenère cipher implementation
- `tests/test_cli.py` - Tests for CLI functionality (to be added)

### Writing Tests

Follow these guidelines when writing tests:

1. **Use descriptive test names** that explain what is being tested
2. **Test both success and failure cases**
3. **Use parametrized tests** for testing multiple inputs
4. **Mock external dependencies** when appropriate
5. **Test edge cases** and boundary conditions

Example test structure:
```python
def test_functionality_description():
    """Test description of what is being tested."""
    # Arrange
    input_data = "test"

    # Act
    result = function_to_test(input_data)

    # Assert
    assert result == expected_output
```

## Code Quality

### Linting and Formatting

```bash
# Check code style
flake8 src/ tests/

# Format code with Black
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/
```

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality:

```bash
# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
```

## CLI Usage

### Basic Commands

```bash
# Show help
dachi --help

# Show Vigenère cipher help
dachi vigenere --help

# Show tool information
dachi info
```

### Vigenère Cipher Examples

#### Standard Encryption/Decryption

```bash
# Encrypt text
dachi vigenere encrypt --key "SECRET" --text "HELLO WORLD"

# Decrypt text
dachi vigenere decrypt --key "SECRET" --text "ZINCS VGXCS"

# Use custom alphabet
dachi vigenere encrypt --key "KEY" --text "HELLO" --alphabet "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
```

#### Autokey Mode

```bash
# Encrypt with autokey
dachi vigenere encrypt --key "SECRET" --text "HELLO WORLD" --autokey

# Decrypt with autokey
dachi vigenere decrypt --key "SECRET" --text "ENCRYPTED_TEXT" --autokey
```

#### File Operations

```bash
# Read from file and encrypt
dachi vigenere encrypt --key "SECRET" --input-file message.txt

# Write output to file
dachi vigenere encrypt --key "SECRET" --text "HELLO" --output-file encrypted.txt

# Read from file and write to file
dachi vigenere encrypt --key "SECRET" --input-file message.txt --output-file encrypted.txt
```

#### Interactive Mode

```bash
# Interactive encryption
dachi vigenere encrypt --key "SECRET" --interactive

# Interactive decryption
dachi vigenere decrypt --key "SECRET" --interactive
```

#### Advanced Options

```bash
# Verbose output with cipher information
dachi vigenere encrypt --key "SECRET" --text "HELLO" --verbose

# Format output with spacing
dachi vigenere encrypt --key "SECRET" --text "HELLO" --format-output

# Analyze alphabet
dachi vigenere analyze --alphabet "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
```

### Programmatic Usage

You can also use the library programmatically:

```python
from dachi.ciphers.vigenere import VigenereCipher
from dachi.core.alphabet import Alphabet

# Create cipher with standard alphabet
cipher = VigenereCipher()

# Encrypt
result = cipher.encrypt("HELLO WORLD", "SECRET")
if result.success:
    print(f"Encrypted: {result}")
else:
    print(f"Error: {result.error_message}")

# Decrypt
result = cipher.decrypt("ZINCS VGXCS", "SECRET")
if result.success:
    print(f"Decrypted: {result}")

# Custom alphabet
alphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
cipher = VigenereCipher(alphabet=alphabet)

# Autokey mode
cipher_autokey = VigenereCipher(autokey=True)
result = cipher_autokey.encrypt("HELLO WORLD", "SECRET")
```

## Project Structure

```
dachi/
├── src/
│   └── dachi/              # Main package
│       ├── __init__.py     # Package initialization
│       ├── cli.py          # CLI interface
│       ├── core/           # Core abstractions
│       │   ├── __init__.py
│       │   ├── alphabet.py # Alphabet management
│       │   ├── cipher.py   # Base cipher classes
│       │   └── key.py      # Key management
│       ├── ciphers/        # Cipher implementations
│       │   ├── __init__.py
│       │   └── vigenere.py # Vigenère cipher
│       └── utils/          # Utilities
│           ├── __init__.py
│           └── text.py     # Text processing
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_alphabet.py
│   └── test_vigenere.py
├── pyproject.toml          # Project configuration
├── README.md              # Main documentation
├── DEVELOPMENT.md         # This file
├── Makefile              # Development commands
├── .pre-commit-config.yaml # Pre-commit hooks
└── .gitignore            # Git ignore rules
```

## Adding New Ciphers

To add a new cipher, follow these steps:

1. **Create a new cipher class** in `src/dachi/ciphers/`
   ```python
   from ..core.cipher import StreamCipher

   class MyCipher(StreamCipher):
       def transform_character(self, char: str, key_char: str) -> str:
           # Implementation here
           pass

       def reverse_transform_character(self, char: str, key_char: str) -> str:
           # Implementation here
           pass
   ```

2. **Add CLI commands** in `src/dachi/cli.py`
   ```python
   @main.group()
   def mycipher() -> None:
       """My Cipher operations."""
       pass

   @mycipher.command()
   def encrypt():
       # Implementation here
       pass
   ```

3. **Add tests** in `tests/test_mycipher.py`
4. **Update documentation** in README.md

## Troubleshooting

### Getting Help

- Check the [main README](README.md) for general information
- Run `dachi --help` for CLI help
- Run `make help` for development commands
- Check test files for usage examples

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Run all checks: `make check-all`
6. Commit your changes: `git commit -m "Add feature"`
7. Push to the branch: `git push origin feature-name`
8. Submit a pull request

## Release Process

1. Update version in `pyproject.toml` and `src/dachi/__init__.py`
2. Update CHANGELOG.md
3. Run all tests: `make test`
4. Build package: `make build`
5. Test installation: `pip install dist/*.whl`