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
from .utils.alphabet_generator import AlphabetGenerator
from .utils.output_formatter import OutputFormatter
from .orchestrator import VigenereOrchestrator


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
@click.option('--text', '-t', help='Text to brute-force decrypt')
@click.option('--input-file', '-i', help='Input file path')
@click.option('--key-length', '-l', required=True, type=int, help='Maximum key length to try')
@click.option('--alphabet', '-a', help='Custom alphabet (default: A-Z)')
@click.option('--autokey', is_flag=True, help='Use autokey mode')
@click.option('--interactive', is_flag=True, help='Interactive mode')
@click.option('--output-dir', '-o', default='out', help='Output directory (default: out)')
@click.option('--base-filename', '-f', help='Base filename for output files (default: brute_force_results)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def brute_force(
    text: Optional[str],
    input_file: Optional[str],
    key_length: int,
    alphabet: Optional[str],
    autokey: bool,
    interactive: bool,
    output_dir: str,
    base_filename: Optional[str],
    verbose: bool,
) -> None:
    """Brute-force decrypt text using all possible keys up to specified length."""

    if key_length <= 0:
        print_error("Key length must be positive")
        return

    if key_length > 6:
        console.print("[yellow]Warning: Large key lengths may take a very long time to complete![/yellow]")
        if not interactive:
            console.print("[yellow]Consider using --interactive to confirm.[/yellow]")

    # Create alphabet
    alphabet_obj = create_alphabet_from_string(alphabet)

    # Create cipher
    cipher = VigenereCipher(alphabet=alphabet_obj, autokey=autokey)

    if verbose:
        display_cipher_info(cipher)
        total_combinations = sum(len(alphabet_obj.characters) ** i for i in range(1, key_length + 1))
        console.print(f"[blue]Total key combinations to try: {total_combinations:,}[/blue]")

    # Get input text
    if interactive:
        if not text:
            text = get_interactive_input("Enter text to brute-force decrypt: ")
    elif input_file:
        text = read_file_content(input_file)
    elif not text:
        print_error("Must provide text via --text, --input-file, or --interactive")
        return

    # Set default base filename if not provided
    if not base_filename:
        base_filename = "brute_force_results"

    # Perform brute-force decryption
    console.print("[blue]Starting brute-force decryption...[/blue]")
    results = cipher.brute_force_decrypt(text, key_length)

    if "error" in results:
        print_error(results["error"])
        return

    # Save results
    try:
        saved_files = OutputFormatter.save_results(results, base_filename, output_dir)

        # Display summary
        console.print(Panel(
            f"Brute-force decryption completed!\n\n"
            f"Total keys tried: {results['total_keys']:,}\n"
            f"Successful decryptions: {results['successful_decryptions']}\n"
            f"Max key length: {results['max_key_length']}\n"
            f"Autokey mode: {results['autokey']}\n\n"
            f"Results saved to:\n"
            f"• TXT: {saved_files['txt']}\n"
            f"• JSON: {saved_files['json']}\n"
            f"• CSV: {saved_files['csv']}",
            title="[green]Brute-Force Results[/green]",
            border_style="green"
        ))

        # Show first few successful results
        successful_results = [r for r in results['results'] if r['success']]
        if successful_results:
            console.print("\n[cyan]First few successful decryptions:[/cyan]")
            for i, result in enumerate(successful_results[:5]):
                console.print(f"  {i+1}. Key: '{result['key']}' -> '{result['decrypted_text']}'")
            if len(successful_results) > 5:
                console.print(f"  ... and {len(successful_results) - 5} more (see output files)")

    except Exception as e:
        print_error(f"Error saving results: {e}")


@vigenere.command()
@click.option('--text', '-t', help='Text to decrypt')
@click.option('--input-file', '-i', help='Input file path')
@click.option('--alphabets-file', '-a', help='File containing list of alphabets (one per line)')
@click.option('--keys-file', '-k', help='File containing list of keys')
@click.option('--key', help='Single key to use')
@click.option('--autokey', is_flag=True, help='Use autokey mode')
@click.option('--interactive', is_flag=True, help='Interactive mode')
@click.option('--output-dir', '-o', default='out', help='Output directory (default: out)')
@click.option('--base-filename', '-f', help='Base filename for output files (default: orchestrate_results)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def orchestrate(
    text: Optional[str],
    input_file: Optional[str],
    alphabets_file: Optional[str],
    keys_file: Optional[str],
    key: Optional[str],
    autokey: bool,
    interactive: bool,
    output_dir: str,
    base_filename: Optional[str],
    verbose: bool,
) -> None:
    """Orchestrate Vigenère decryption over all key/alphabet permutations."""

    # Validate inputs
    if not alphabets_file and not keys_file and not key:
        print_error("Must provide either --alphabets-file, --keys-file, or --key")
        return

    if keys_file and key:
        print_error("Cannot provide both --keys-file and --key")
        return

    # Create orchestrator
    orchestrator = VigenereOrchestrator(autokey=autokey)

    # Load alphabets and keys
    try:
        alphabets = orchestrator.load_alphabets(alphabets_file)
        keys = orchestrator.load_keys(keys_file, key)

        if verbose:
            console.print(f"[blue]Loaded {len(alphabets)} alphabets and {len(keys)} keys[/blue]")
            if alphabets_file:
                console.print(f"[blue]Alphabets file: {alphabets_file}[/blue]")
            if keys_file:
                console.print(f"[blue]Keys file: {keys_file}[/blue]")
            elif key:
                console.print(f"[blue]Single key: {key}[/blue]")
    except Exception as e:
        print_error(f"Error loading alphabets or keys: {e}")
        return

    # Get input text
    if interactive:
        if not text:
            text = get_interactive_input("Enter text to decrypt: ")
    elif input_file:
        text = read_file_content(input_file)
    elif not text:
        print_error("Must provide text via --text, --input-file, or --interactive")
        return

    # Set default base filename if not provided
    if not base_filename:
        base_filename = "orchestrate_results"

    # Run orchestration
    console.print("[blue]Starting orchestrated decryption...[/blue]")
    results = orchestrator.run(text, alphabets, keys)

    # Save results
    try:
        saved_files = orchestrator.output_results(results, base_filename, output_dir)

        # Display summary
        total_attempts = len(results['results'])
        successful = sum(1 for r in results['results'] if r['success'])

        console.print(Panel(
            f"Orchestrated decryption completed!\n\n"
            f"Total attempts: {total_attempts:,}\n"
            f"Successful decryptions: {successful}\n"
            f"Alphabets used: {results['total_alphabets']}\n"
            f"Keys used: {results['total_keys']}\n"
            f"Autokey mode: {results['autokey']}\n\n"
            f"Results saved to:\n"
            f"• TXT: {saved_files['txt']}\n"
            f"• JSON: {saved_files['json']}\n"
            f"• CSV: {saved_files['csv']}",
            title="[green]Orchestration Results[/green]",
            border_style="green"
        ))

        # Show first few successful results
        successful_results = [r for r in results['results'] if r['success']]
        if successful_results:
            console.print("\n[cyan]First few successful decryptions:[/cyan]")
            for i, result in enumerate(successful_results[:5]):
                console.print(f"  {i+1}. Key: '{result['key']}' | Alphabet: '{result['alphabet'][:10]}...' -> '{result['decrypted_text']}'")
            if len(successful_results) > 5:
                console.print(f"  ... and {len(successful_results) - 5} more (see output files)")

    except Exception as e:
        print_error(f"Error saving results: {e}")


@main.group()
def alphabet() -> None:
    """Alphabet generation and manipulation operations."""
    pass


@alphabet.command()
@click.option('--input-file', '-i', required=True, help='Input file path containing words/phrases')
@click.option('--output-file', '-o', help='Output file path for the generated alphabet')
@click.option('--base-alphabet', '-b', default='ABCDEFGHIJKLMNOPQRSTUVWXYZ',
              help='Base alphabet to use for remaining characters (default: A-Z)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def generate(input_file: str, output_file: Optional[str], base_alphabet: str, verbose: bool) -> None:
    """Generate a keyed alphabet from a word list file."""

    try:
        # Generate the alphabet
        alphabet_obj = AlphabetGenerator.create_alphabet_from_file(input_file, base_alphabet)

        if verbose:
            # Parse the words to show what was used
            words = AlphabetGenerator.parse_word_list(input_file)
            console.print(f"[blue]Parsed words: {', '.join(words)}[/blue]")

        # Display the result
        table = Table(title="Generated Keyed Alphabet")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Input File", input_file)
        table.add_row("Generated Alphabet", alphabet_obj.characters)
        table.add_row("Length", str(len(alphabet_obj)))
        table.add_row("Base Alphabet", base_alphabet)

        console.print(table)

        # Save to file if requested
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(alphabet_obj.characters)
            print_success(f"Alphabet saved to: {output_file}")

    except FileNotFoundError as e:
        print_error(str(e))
    except ValueError as e:
        print_error(str(e))
    except Exception as e:
        print_error(f"Unexpected error: {e}")


@alphabet.command()
@click.option('--input-file', '-i', required=True, help='Input file path containing words/phrases')
@click.option('--output-dir', '-o', help='Output directory for generated alphabets')
@click.option('--base-alphabet', '-b', default='ABCDEFGHIJKLMNOPQRSTUVWXYZ',
              help='Base alphabet to use for remaining characters (default: A-Z)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def generate_multiple(input_file: str, output_dir: Optional[str], base_alphabet: str, verbose: bool) -> None:
    """Generate multiple alphabets from a word list file (one per word/phrase)."""

    try:
        # Generate multiple alphabets
        alphabets = AlphabetGenerator.generate_multiple_alphabets(input_file, base_alphabet)
        words = AlphabetGenerator.parse_word_list(input_file)

        if verbose:
            console.print(f"[blue]Generated {len(alphabets)} alphabets from {len(words)} words[/blue]")

        # Display results
        table = Table(title="Generated Alphabets")
        table.add_column("Word/Phrase", style="cyan")
        table.add_column("Generated Alphabet", style="green")
        table.add_column("Length", style="yellow")

        for word, alphabet_obj in zip(words, alphabets):
            table.add_row(word, alphabet_obj.characters, str(len(alphabet_obj)))

        console.print(table)

        # Save to files if requested
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            for i, (word, alphabet_obj) in enumerate(zip(words, alphabets)):
                # Create a safe filename
                safe_word = "".join(c for c in word if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_word = safe_word.replace(' ', '_')
                filename = f"alphabet_{i+1:02d}_{safe_word}.txt"
                filepath = output_path / filename

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"Word: {word}\n")
                    f.write(f"Alphabet: {alphabet_obj.characters}\n")
                    f.write(f"Length: {len(alphabet_obj)}\n")

            print_success(f"Generated {len(alphabets)} alphabet files in: {output_dir}")

    except FileNotFoundError as e:
        print_error(str(e))
    except ValueError as e:
        print_error(str(e))
    except Exception as e:
        print_error(f"Unexpected error: {e}")


@alphabet.command()
@click.option('--words', '-w', required=True, help='Comma-separated list of words/phrases')
@click.option('--base-alphabet', '-b', default='ABCDEFGHIJKLMNOPQRSTUVWXYZ',
              help='Base alphabet to use for remaining characters (default: A-Z)')
@click.option('--output-file', '-o', help='Output file path for the generated alphabet')
def generate_from_words(words: str, base_alphabet: str, output_file: Optional[str]) -> None:
    """Generate a keyed alphabet from a comma-separated list of words."""

    try:
        # Parse words
        word_list = [word.strip() for word in words.split(',') if word.strip()]

        if not word_list:
            print_error("No valid words provided")
            return

        # Generate the alphabet
        keyed_alphabet = AlphabetGenerator.generate_keyed_alphabet(word_list, base_alphabet)
        alphabet_obj = Alphabet(characters=keyed_alphabet)

        # Display the result
        table = Table(title="Generated Keyed Alphabet")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Input Words", words)
        table.add_row("Generated Alphabet", alphabet_obj.characters)
        table.add_row("Length", str(len(alphabet_obj)))
        table.add_row("Base Alphabet", base_alphabet)

        console.print(table)

        # Save to file if requested
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(alphabet_obj.characters)
            print_success(f"Alphabet saved to: {output_file}")

    except ValueError as e:
        print_error(str(e))
    except Exception as e:
        print_error(f"Unexpected error: {e}")


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