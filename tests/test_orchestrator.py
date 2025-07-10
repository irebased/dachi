import os
import tempfile
import pytest
from dachi.orchestrator import VigenereOrchestrator
from dachi.core.alphabet import Alphabet

def test_load_alphabets_with_file():
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write("ABC\nDEF\nGHI")
        tmp.flush()
        path = tmp.name
    try:
        orchestrator = VigenereOrchestrator()
        alphabets = orchestrator.load_alphabets(path)
        assert len(alphabets) == 3
        assert alphabets[0].characters == "ABC"
        assert alphabets[1].characters == "DEF"
        assert alphabets[2].characters == "GHI"
    finally:
        os.remove(path)

def test_load_alphabets_without_file():
    orchestrator = VigenereOrchestrator()
    alphabets = orchestrator.load_alphabets(None)
    assert len(alphabets) == 1
    assert alphabets[0].characters == "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def test_load_keys_with_file():
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write("KEY1\nKEY2\nKEY3")
        tmp.flush()
        path = tmp.name
    try:
        orchestrator = VigenereOrchestrator()
        keys = orchestrator.load_keys(path, None)
        assert keys == ["KEY1", "KEY2", "KEY3"]
    finally:
        os.remove(path)

def test_load_keys_with_single_key():
    orchestrator = VigenereOrchestrator()
    keys = orchestrator.load_keys(None, "SINGLE_KEY")
    assert keys == ["SINGLE_KEY"]

def test_load_keys_no_keys():
    orchestrator = VigenereOrchestrator()
    with pytest.raises(ValueError, match="No keys provided"):
        orchestrator.load_keys(None, None)

def test_run_orchestration():
    orchestrator = VigenereOrchestrator()
    alphabets = [Alphabet(characters="ABC"), Alphabet(characters="DEF")]
    keys = ["A", "B"]
    ciphertext = "ABC"  # Encrypted with key "A" in alphabet "ABC"

    results = orchestrator.run(ciphertext, alphabets, keys)

    assert results["ciphertext"] == "ABC"
    assert results["total_alphabets"] == 2
    assert results["total_keys"] == 2
    assert len(results["results"]) == 4  # 2 alphabets × 2 keys

    # Check that we have results for each combination
    alphabet_chars = [r["alphabet"] for r in results["results"]]
    key_chars = [r["key"] for r in results["results"]]
    assert "ABC" in alphabet_chars
    assert "DEF" in alphabet_chars
    assert "A" in key_chars
    assert "B" in key_chars

def test_run_orchestration_autokey():
    orchestrator = VigenereOrchestrator(autokey=True)
    alphabets = [Alphabet(characters="ABC")]
    keys = ["A"]
    ciphertext = "ABC"

    results = orchestrator.run(ciphertext, alphabets, keys)

    assert results["autokey"] is True
    assert len(results["results"]) == 1

def test_output_results():
    orchestrator = VigenereOrchestrator()
    alphabets = [Alphabet(characters="ABC")]
    keys = ["A"]
    ciphertext = "ABC"

    # Use the actual orchestrator to generate results
    results = orchestrator.run(ciphertext, alphabets, keys)

    with tempfile.TemporaryDirectory() as tmpdir:
        saved_files = orchestrator.output_results(results, "test_orchestrate", tmpdir)

        assert os.path.exists(saved_files["txt"])
        assert os.path.exists(saved_files["json"])
        assert os.path.exists(saved_files["csv"])

        # Check that files contain expected content
        with open(saved_files["txt"]) as f:
            content = f.read()
            assert "ABC" in content
            assert "Key: A" in content