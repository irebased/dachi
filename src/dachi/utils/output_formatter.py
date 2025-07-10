"""Output formatting utilities for brute-force decryption results."""

import json
import csv
from pathlib import Path
from typing import Dict, Any, List


class OutputFormatter:
    """Formats brute-force decryption results to various output formats."""

    @staticmethod
    def format_txt(results: Dict[str, Any]) -> str:
        """Format results as plain text.

        Args:
            results: Brute-force decryption results

        Returns:
            Formatted text string
        """
        if "error" in results:
            return f"Error: {results['error']}"

        lines = []
        lines.append("=" * 60)
        lines.append("BRUTE-FORCE DECRYPTION RESULTS")
        lines.append("=" * 60)
        lines.append(f"Ciphertext: {results['ciphertext']}")
        lines.append(f"Max Key Length: {results['max_key_length']}")
        lines.append(f"Autokey Mode: {results['autokey']}")
        lines.append(f"Alphabet: {results['alphabet']}")
        lines.append(f"Total Keys Tried: {results['total_keys']}")
        lines.append(f"Successful Decryptions: {results['successful_decryptions']}")
        lines.append("")
        lines.append("RESULTS:")
        lines.append("-" * 60)

        for result in results['results']:
            if result['success']:
                lines.append(f"Key: {result['key']} (length: {result['key_length']})")
                lines.append(f"Decrypted: {result['decrypted_text']}")
                lines.append("")
            else:
                lines.append(f"Key: {result['key']} (length: {result['key_length']}) - FAILED")
                if 'error' in result:
                    lines.append(f"Error: {result['error']}")
                lines.append("")

        return "\n".join(lines)

    @staticmethod
    def format_json(results: Dict[str, Any]) -> str:
        """Format results as JSON.

        Args:
            results: Brute-force decryption results

        Returns:
            JSON string
        """
        return json.dumps(results, indent=2, ensure_ascii=False)

    @staticmethod
    def format_csv(results: Dict[str, Any]) -> str:
        """Format results as CSV.

        Args:
            results: Brute-force decryption results

        Returns:
            CSV string
        """
        if "error" in results:
            return f"Error,{results['error']}"

        # Create CSV content using StringIO
        import io
        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow([
            "Key", "Key Length", "Success", "Decrypted Text", "Error"
        ])

        # Data rows
        for result in results['results']:
            writer.writerow([
                result['key'],
                result['key_length'],
                result['success'],
                result.get('decrypted_text', ''),
                result.get('error', '')
            ])

        return output.getvalue()

    @staticmethod
    def save_results(results: Dict[str, Any], base_filename: str, output_dir: str = "out") -> Dict[str, str]:
        """Save results in all formats (TXT, JSON, CSV).

        Args:
            results: Brute-force decryption results
            base_filename: Base filename (without extension)
            output_dir: Output directory (default: "out")

        Returns:
            Dictionary mapping format to file path
        """
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        saved_files = {}

        # Save TXT
        txt_content = OutputFormatter.format_txt(results)
        txt_path = output_path / f"{base_filename}.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        saved_files['txt'] = str(txt_path)

        # Save JSON
        json_content = OutputFormatter.format_json(results)
        json_path = output_path / f"{base_filename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(json_content)
        saved_files['json'] = str(json_path)

        # Save CSV
        csv_content = OutputFormatter.format_csv(results)
        csv_path = output_path / f"{base_filename}.csv"
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        saved_files['csv'] = str(csv_path)

        return saved_files