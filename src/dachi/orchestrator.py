"""Orchestrator for Vigenère brute-force and permutation attacks."""

from typing import List, Optional, Dict, Any
from .core.alphabet import Alphabet
from .ciphers.vigenere import VigenereCipher
from .utils.alphabet_generator import AlphabetGenerator
from .utils.key_generator import parse_key_list
from .utils.output_formatter import OutputFormatter

class VigenereOrchestrator:
    """Orchestrates Vigenère decryption over all key/alphabet permutations."""
    def __init__(self, autokey: bool = False):
        self.autokey = autokey

    def load_alphabets(self, file_path: Optional[str]) -> List[Alphabet]:
        if file_path:
            # Each line/entry is a full alphabet string
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
            return [Alphabet(characters=line) for line in lines]
        else:
            return [Alphabet.standard_english()]

    def load_keys(self, file_path: Optional[str], key: Optional[str]) -> List[str]:
        if file_path:
            return parse_key_list(file_path)
        elif key:
            return [key]
        else:
            raise ValueError("No keys provided")

    def run(self, ciphertext: str, alphabets: List[Alphabet], keys: List[str]) -> Dict[str, Any]:
        results = {
            "ciphertext": ciphertext,
            "autokey": self.autokey,
            "max_key_length": max(len(key) for key in keys) if keys else 0,
            # Removed top-level 'alphabet' field
            "total_alphabets": len(alphabets),
            "total_keys": len(keys),
            "successful_decryptions": 0,
            "results": []
        }

        successful_count = 0
        for alphabet in alphabets:
            cipher = VigenereCipher(alphabet=alphabet, autokey=self.autokey)
            for key in keys:
                result = cipher.decrypt(ciphertext, key)
                if result.success:
                    successful_count += 1
                results["results"].append({
                    "alphabet": alphabet.characters,
                    "key": key,
                    "key_length": len(key),
                    "success": result.success,
                    "decrypted_text": str(result) if result.success else "",
                    "error": result.error_message if not result.success else None
                })

        results["successful_decryptions"] = successful_count
        return results

    def output_results(self, results: Dict[str, Any], base_filename: str, output_dir: str = "out") -> Dict[str, str]:
        return OutputFormatter.save_results(results, base_filename, output_dir)