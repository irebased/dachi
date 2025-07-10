# Dachi - Cryptographic CLI Tool

A powerful command-line tool for cryptographic operations, featuring a highly extensible architecture with strong abstraction layers.

## Features

- **Vigenère Cipher**: Classic and autokey variants with custom alphabets
- **Brute Force Decryption**: Try all possible keys up to a specified length
- **Orchestrated Attacks**: Test multiple alphabets and keys simultaneously
- **Alphabet Generation**: Create keyed alphabets from word lists
- **Key Generation**: Parse and manage key lists from files
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

> **Note:** All input text is automatically converted to uppercase before processing. For example, `hello world` becomes `HELLO WORLD` internally. This ensures consistent encryption and decryption regardless of input case.

# Read from file
dachi vigenere encrypt --key "SECRET" --input-file message.txt --output-file encrypted.txt

# Interactive mode
dachi vigenere encrypt --key "SECRET" --interactive
```

#### Brute Force Decryption

```bash
# Try all keys up to length 3
dachi vigenere brute-force --text "ZINCS VGXCS" --key-length 3

# Use autokey mode
dachi vigenere brute-force --text "ZINCS VGXCS" --key-length 3 --autokey

# Read from file and specify output directory
dachi vigenere brute-force --input-file encrypted.txt --key-length 4 --output-dir results

# Use custom alphabet
dachi vigenere brute-force --text "ZINCS VGXCS" --key-length 2 --alphabet "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
```

### Alphabet Generation

#### Generate Single Alphabet from File

```bash
# Generate alphabet from words in a file
dachi alphabet generate --input-file words.txt --output-file custom_alphabet.txt

# Use different base alphabet
dachi alphabet generate --input-file words.txt --base-alphabet "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
```

**Input File Format**: The file can contain words/phrases separated by:
- Commas: `SECRET, KEY, PASSWORD`
- Spaces: `SECRET KEY PASSWORD`
- Newlines:
  ```
  SECRET
  KEY
  PASSWORD
  ```

#### Generate Multiple Alphabets

```bash
# Generate one alphabet per word/phrase
dachi alphabet generate-multiple --input-file words.txt --output-dir alphabets/
```

#### Generate from Command Line

```bash
# Generate from comma-separated words
dachi alphabet generate-from-words --words "SECRET,KEY,PASSWORD" --output-file alphabet.txt
```

### Orchestrated Decryption

The orchestrator allows you to test multiple alphabets and keys simultaneously, perfect for cryptanalysis scenarios.

#### Basic Orchestration

```bash
# Test all keys from a file against the standard alphabet
dachi vigenere orchestrate --text "ZINCS VGXCS" --keys-file keys.txt

# Test a single key against multiple alphabets
dachi vigenere orchestrate --text "ZINCS VGXCS" --key "SECRET" --alphabets-file alphabets.txt
```

#### Advanced Orchestration

```bash
# Test all combinations of alphabets and keys
dachi vigenere orchestrate --text "ZINCS VGXCS" --alphabets-file alphabets.txt --keys-file keys.txt

# Use autokey mode
dachi vigenere orchestrate --text "ZINCS VGXCS" --keys-file keys.txt --autokey

# Specify output directory and filename
dachi vigenere orchestrate --text "ZINCS VGXCS" --keys-file keys.txt --output-dir results --base-filename attack_results
```

#### Input File Formats

**Alphabets File**: Each line contains a complete alphabet string
```
ABCDEFGHIJKLMNOPQRSTUVWXYZ
SECRETKEYABCDFGHIJLMNOPQUVWXYZ
CUSTOMALPHABET123
```

**Keys File**: Keys separated by commas, spaces, or newlines
```
SECRET, KEY, PASSWORD
SECRET
KEY
PASSWORD
```

#### Orchestration Scenarios

1. **Single Key, Multiple Alphabets**: Test if a known key works with different alphabet arrangements
   ```bash
   dachi vigenere orchestrate --text "ciphertext" --key "KNOWNKEY" --alphabets-file alphabets.txt
   ```

2. **Multiple Keys, Single Alphabet**: Try different keys against the standard alphabet
   ```bash
   dachi vigenere orchestrate --text "ciphertext" --keys-file keys.txt
   ```

3. **All Combinations**: Exhaustive testing of all key-alphabet combinations
   ```bash
   dachi vigenere orchestrate --text "ciphertext" --alphabets-file alphabets.txt --keys-file keys.txt
   ```

4. **Autokey Analysis**: Test autokey mode with various keys
   ```bash
   dachi vigenere orchestrate --text "ciphertext" --keys-file keys.txt --autokey
   ```

### Output Formats

The orchestrator and brute force commands generate multiple output formats:

- **TXT**: Human-readable summary with all results
- **JSON**: Structured data for programmatic analysis
- **CSV**: Tabular format for spreadsheet analysis

Files are saved in the specified output directory with descriptive names.

## Examples

### Example 1: Basic Cryptanalysis

```bash
# Create a keyed alphabet from common words
echo "SECRET, KEY, PASSWORD" > words.txt
dachi alphabet generate --input-file words.txt --output-file custom_alphabet.txt

# Create a list of potential keys
echo "SECRET, KEY, PASSWORD, TEST, HELLO" > keys.txt

# Try to decrypt with custom alphabet and key list
dachi vigenere orchestrate --text "encrypted_message" --alphabets-file custom_alphabet.txt --keys-file keys.txt
```

### Example 2: Brute Force Attack

```bash
# Try all possible 3-letter keys
dachi vigenere brute-force --text "encrypted_message" --key-length 3 --output-dir attack_results

# Check results
ls attack_results/
# Output: brute_force_results.txt, brute_force_results.json, brute_force_results.csv
```

### Example 3: Multiple Alphabet Testing

```bash
# Create multiple alphabets from different word sets
echo "SECRET, KEY" > words1.txt
echo "PASSWORD, LOGIN" > words2.txt
echo "ADMIN, ROOT" > words3.txt

# Generate alphabets
dachi alphabet generate-multiple --input-file words1.txt --output-dir alphabets/
dachi alphabet generate-multiple --input-file words2.txt --output-dir alphabets/
dachi alphabet generate-multiple --input-file words3.txt --output-dir alphabets/

# Test all alphabets with a known key
dachi vigenere orchestrate --text "encrypted_message" --key "KNOWNKEY" --alphabets-file alphabets/alphabets.txt
```

### Example 4: Autokey Analysis

```bash
# Test autokey mode with various keys
echo "SECRET, KEY, PASSWORD" > keys.txt
dachi vigenere orchestrate --text "autokey_encrypted_message" --keys-file keys.txt --autokey
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

# Brute force decryption
results = cipher.brute_force_decrypt("ZINCS VGXCS", 3)
print(f"Found {results['successful_decryptions']} successful decryptions")

# Alphabet generation
from dachi.utils.alphabet_generator import AlphabetGenerator
keyed_alphabet = AlphabetGenerator.generate_keyed_alphabet(["SECRET", "KEY"], "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
alphabet_obj = Alphabet(characters=keyed_alphabet)

# Key parsing
from dachi.utils.key_generator import parse_key_list
keys = parse_key_list("keys.txt")
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
- **`dachi.orchestrator`**: Orchestrated decryption across multiple alphabets and keys
- **`dachi.utils.alphabet_generator`**: Generate keyed alphabets from word lists
- **`dachi.utils.key_generator`**: Parse and manage key lists from files
- **`dachi.utils.output_formatter`**: Format results to various output formats

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
│       ├── orchestrator.py     # Orchestrated decryption
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
│           ├── text.py         # Text processing
│           ├── alphabet_generator.py  # Alphabet generation
│           ├── key_generator.py       # Key parsing
│           └── output_formatter.py    # Output formatting
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