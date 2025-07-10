import os
import tempfile
import pytest
from dachi.utils.alphabet_generator import AlphabetGenerator

@pytest.mark.parametrize("content,expected", [
    ("HELLO, WORLD, CRYPTO", ["HELLO", "WORLD", "CRYPTO"]),
    ("HELLO\nWORLD\nCRYPTO", ["HELLO", "WORLD", "CRYPTO"]),
    ("HELLO WORLD CRYPTO", ["HELLO", "WORLD", "CRYPTO"]),
    ("  HELLO ,  WORLD ,CRYPTO  ", ["HELLO", "WORLD", "CRYPTO"]),
    ("  HELLO \n  WORLD \nCRYPTO  ", ["HELLO", "WORLD", "CRYPTO"]),
])
def test_parse_word_list(content, expected):
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(content)
        tmp.flush()
        path = tmp.name
    try:
        result = AlphabetGenerator.parse_word_list(path)
        assert result == expected
    finally:
        os.remove(path)

@pytest.mark.parametrize("words,base,expected", [
    (["HELLO"], "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "HELOABCDFGIJKMNPQRSTUVWXYZ"),
    (["WORLD"], "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "WORLDABCEFGHIJKMNPQSTUVXYZ"),
    (["CRYPTO"], "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "CRYPTOABDEFGHIJKLMNQSUVWXZ"),
    (["HELLO", "WORLD"], "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "HELOWRDABCFGIJKMNPQSTUVXYZ"),
])
def test_generate_keyed_alphabet(words, base, expected):
    result = AlphabetGenerator.generate_keyed_alphabet(words, base)
    assert result == expected