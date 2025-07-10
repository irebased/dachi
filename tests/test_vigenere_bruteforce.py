import os
import tempfile
import json
import csv
import pytest
from dachi.ciphers.vigenere import VigenereCipher
from dachi.core.alphabet import Alphabet
from dachi.utils.output_formatter import OutputFormatter

def test_generate_all_keys_small():
    alphabet = Alphabet(characters="AB")
    cipher = VigenereCipher(alphabet=alphabet)
    keys = cipher.generate_all_keys(2)
    # 2^1 + 2^2 = 2 + 4 = 6 keys
    assert set(keys) == {"A", "B", "AA", "AB", "BA", "BB"}

def test_brute_force_decrypt_basic():
    alphabet = Alphabet(characters="ABC")
    cipher = VigenereCipher(alphabet=alphabet)
    # Encrypt 'ABC' with key 'A' (should be itself)
    encrypted = cipher.encrypt("ABC", "A")
    results = cipher.brute_force_decrypt(str(encrypted), 1)
    found = any(r['key'] == 'A' and r['decrypted_text'] == 'ABC' for r in results['results'])
    assert found

def test_brute_force_decrypt_autokey():
    alphabet = Alphabet(characters="ABC")
    cipher = VigenereCipher(alphabet=alphabet, autokey=True)
    encrypted = cipher.encrypt("ABC", "A")
    results = cipher.brute_force_decrypt(str(encrypted), 1)
    found = any(r['key'] == 'A' and r['decrypted_text'] == 'ABC' for r in results['results'])
    assert found

def test_output_formatter_all_formats():
    # Minimal fake result set
    results = {
        "ciphertext": "XYZ",
        "max_key_length": 1,
        "autokey": False,
        "alphabet": "ABC",
        "total_keys": 2,
        "successful_decryptions": 1,
        "results": [
            {"key": "A", "key_length": 1, "decrypted_text": "XYZ", "success": True},
            {"key": "B", "key_length": 1, "decrypted_text": "", "success": False, "error": "fail"},
        ]
    }
    txt = OutputFormatter.format_txt(results)
    assert "Key: A" in txt and "Decrypted: XYZ" in txt
    js = OutputFormatter.format_json(results)
    assert json.loads(js)["ciphertext"] == "XYZ"
    csv_str = OutputFormatter.format_csv(results)
    assert "Key,Key Length,Success,Decrypted Text,Error" in csv_str
    assert "A,1,True,XYZ," in csv_str or "A,1,True,XYZ,\r\n" in csv_str

def test_output_formatter_save_results():
    results = {
        "ciphertext": "XYZ",
        "max_key_length": 1,
        "autokey": False,
        "alphabet": "ABC",
        "total_keys": 2,
        "successful_decryptions": 1,
        "results": [
            {"key": "A", "key_length": 1, "decrypted_text": "XYZ", "success": True},
            {"key": "B", "key_length": 1, "decrypted_text": "", "success": False, "error": "fail"},
        ]
    }
    with tempfile.TemporaryDirectory() as tmpdir:
        files = OutputFormatter.save_results(results, "test_brute", tmpdir)
        assert os.path.exists(files['txt'])
        assert os.path.exists(files['json'])
        assert os.path.exists(files['csv'])
        # Check content
        with open(files['json']) as f:
            data = json.load(f)
            assert data["ciphertext"] == "XYZ"
        with open(files['csv']) as f:
            reader = csv.reader(f)
            header = next(reader)
            assert header[0] == "Key"