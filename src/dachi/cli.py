"""Command-line interface for the Dachi cryptographic tool."""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .core.alphabet import Alphabet
from .ciphers.vigenere import VigenereCipher
from .utils.text import format_output


console = Console()


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[red]Error: {message}[/red]")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[green]{message}[/green]")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[blue]{message}[/blue]")


def create_alphabet_from_string(alphabet_str: Optional[str]) -> Alphabet:
    """Create an alphabet from a string or use default."""
    if alphabet_str:
        try:
            return Alphabet(characters=alphabet_str)
        except ValueError as e:
            print_error(f"Invalid alphabet: {e}")
            return Alphabet.standard_english()
    else:
        return Alphabet.standard_english()


def read_file_content(file_path: str) -> str:
    """Read content from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print_error(f"File not found: {file_path}")
        return ""
    except Exception as e:
        print_error(f"Error reading file: {e}")
        return ""


def write_file_content(file_path: str, content: str) -> None:
    """Write content to a file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print_success(f"Output written to: {file_path}")
    except Exception as e:
        print_error(f"Error writing file: {e}")


def get_interactive_input(prompt: str) -> str:
    """Get input interactively from the user."""
    return input(prompt).strip()


def display_cipher_info(cipher: VigenereCipher) -> None:
    """Display information about the cipher."""
    table = Table(title="Cipher Information")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Type", "Vigenère Cipher")
    table.add_row("Alphabet Size", str(len(cipher.alphabet)))
    table.add_row("Alphabet", cipher.alphabet.characters)
    table.add_row("Case Sensitive", str(cipher.alphabet.case_sensitive))
    table.add_row("Autokey Mode", str(cipher.autokey))

    console.print(table)


@click.group()
@click.version_option(version="0.1.0", prog_name="dachi")
def main() -> None:
    """Dachi - A powerful cryptographic CLI tool with extensible architecture.

    This tool provides various cryptographic operations with support for
    custom alphabets and advanced features like autokey mode.
    """
    pass


@main.group()
def vigenere() -> None:
    """Vigenère cipher operations."""
    pass


@vigenere.command()
@click.option('--key', '-k', required=True, help='Encryption key')
@click.option('--text', '-t', help='Text to encrypt')
@click.option('--input-file', '-i', help='Input file path')
@click.option('--output-file', '-o', help='Output file path')
@click.option('--alphabet', '-a', help='Custom alphabet (default: A-Z)')
@click.option('--autokey', is_flag=True, help='Use autokey mode')
@click.option('--interactive', is_flag=True, help='Interactive mode')
@click.option('--format-output', is_flag=True, help='Format output with spacing')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def encrypt(
    key: str,
    text: Optional[str],
    input_file: Optional[str],
    output_file: Optional[str],
    alphabet: Optional[str],
    autokey: bool,
    interactive: bool,
    format_output: bool,
    verbose: bool,
) -> None:
    """Encrypt text using Vigenère cipher."""

    # Create alphabet
    alphabet_obj = create_alphabet_from_string(alphabet)

    # Create cipher
    cipher = VigenereCipher(alphabet=alphabet_obj, autokey=autokey)

    if verbose:
        display_cipher_info(cipher)

    # Get input text
    if interactive:
        if not text:
            text = get_interactive_input("Enter text to encrypt: ")
    elif input_file:
        text = read_file_content(input_file)
    elif not text:
        print_error("Must provide text via --text, --input-file, or --interactive")
        return

    # Perform encryption
    result = cipher.encrypt(text, key)

    if not result.success:
        print_error(result.error_message or "Encryption failed")
        return

    # Format and display result
    output_text = str(result)
    if format_output:
        output_text = format_output(output_text)

    if output_file:
        write_file_content(output_file, output_text)
    else:
        console.print(Panel(
            output_text,
            title="[green]Encrypted Text[/green]",
            border_style="green"
        ))


@vigenere.command()
@click.option('--key', '-k', required=True, help='Decryption key')
@click.option('--text', '-t', help='Text to decrypt')
@click.option('--input-file', '-i', help='Input file path')
@click.option('--output-file', '-o', help='Output file path')
@click.option('--alphabet', '-a', help='Custom alphabet (default: A-Z)')
@click.option('--autokey', is_flag=True, help='Use autokey mode')
@click.option('--interactive', is_flag=True, help='Interactive mode')
@click.option('--format-output', is_flag=True, help='Format output with spacing')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def decrypt(
    key: str,
    text: Optional[str],
    input_file: Optional[str],
    output_file: Optional[str],
    alphabet: Optional[str],
    autokey: bool,
    interactive: bool,
    format_output: bool,
    verbose: bool,
) -> None:
    """Decrypt text using Vigenère cipher."""

    # Create alphabet
    alphabet_obj = create_alphabet_from_string(alphabet)

    # Create cipher
    cipher = VigenereCipher(alphabet=alphabet_obj, autokey=autokey)

    if verbose:
        display_cipher_info(cipher)

    # Get input text
    if interactive:
        if not text:
            text = get_interactive_input("Enter text to decrypt: ")
    elif input_file:
        text = read_file_content(input_file)
    elif not text:
        print_error("Must provide text via --text, --input-file, or --interactive")
        return

    # Perform decryption
    result = cipher.decrypt(text, key)

    if not result.success:
        print_error(result.error_message or "Decryption failed")
        return

    # Format and display result
    output_text = str(result)
    if format_output:
        output_text = format_output(output_text)

    if output_file:
        write_file_content(output_file, output_text)
    else:
        console.print(Panel(
            output_text,
            title="[green]Decrypted Text[/green]",
            border_style="green"
        ))


@vigenere.command()
@click.option('--alphabet', '-a', help='Custom alphabet to analyze')
def analyze(alphabet: Optional[str]) -> None:
    """Analyze alphabet properties."""

    alphabet_obj = create_alphabet_from_string(alphabet)

    table = Table(title="Alphabet Analysis")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Characters", alphabet_obj.characters)
    table.add_row("Length", str(len(alphabet_obj)))
    table.add_row("Case Sensitive", str(alphabet_obj.case_sensitive))
    table.add_row("Unique Characters", str(len(set(alphabet_obj.characters))))

    # Character frequency analysis
    char_count = {}
    for char in alphabet_obj.characters:
        char_count[char] = char_count.get(char, 0) + 1

    duplicates = [char for char, count in char_count.items() if count > 1]
    if duplicates:
        table.add_row("Duplicate Characters", ", ".join(duplicates))
    else:
        table.add_row("Duplicate Characters", "None")

    console.print(table)


@main.command()
def info() -> None:
    """Display information about the Dachi tool."""

    console.print(Panel(
        Text.assemble(
            ("Dachi", "bold blue"),
            " - A powerful cryptographic CLI tool\n\n",
            ("Features:", "bold"),
            "\n• Vigenère cipher with autokey support",
            "\n• Custom alphabets",
            "\n• Extensible architecture",
            "\n• Rich CLI interface",
            "\n• Type safety with Pydantic",
            "\n\n",
            ("Version:", "bold"),
            " 0.1.0",
            "\n",
            ("Author:", "bold"),
            " Your Name",
        ),
        title="[bold blue]Dachi Cryptographic Tool[/bold blue]",
        border_style="blue"
    ))


if __name__ == "__main__":
    main()