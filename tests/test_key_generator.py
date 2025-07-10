import os
import tempfile
import pytest
from dachi.utils.key_generator import parse_key_list

@pytest.mark.parametrize("content,expected", [
    ("KEY1, KEY2, KEY3", ["KEY1", "KEY2", "KEY3"]),
    ("KEY1\nKEY2\nKEY3", ["KEY1", "KEY2", "KEY3"]),
    ("KEY1 KEY2 KEY3", ["KEY1", "KEY2", "KEY3"]),
    ("  KEY1 ,  KEY2 ,KEY3  ", ["KEY1", "KEY2", "KEY3"]),
    ("  KEY1 \n  KEY2 \nKEY3  ", ["KEY1", "KEY2", "KEY3"]),
    ("KEY1,KEY2,KEY1,KEY3", ["KEY1", "KEY2", "KEY3"]),
    ("KEY1 KEY2 KEY1 KEY3", ["KEY1", "KEY2", "KEY3"]),
    ("KEY1\nKEY2\nKEY1\nKEY3", ["KEY1", "KEY2", "KEY3"]),
    ("KEY1", ["KEY1"]),
    ("   KEY1   ", ["KEY1"]),
])
def test_parse_key_list(content, expected):
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(content)
        tmp.flush()
        path = tmp.name
    try:
        result = parse_key_list(path)
        assert result == expected
    finally:
        os.remove(path)