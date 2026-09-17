import unittest

from jkUnicode.uniScript import get_script


class TestUniScript(unittest.TestCase):
    def test_get_script_0x4ff(self) -> None:
        assert get_script(0x4FF) == "Cyrillic"

    def test_get_script_0x500(self) -> None:
        assert get_script(0x500) == "Cyrillic"

    def test_get_script_unknown(self) -> None:
        assert get_script(0xF000) == "Unknown"

    def test_get_script_last(self) -> None:
        assert get_script(0xE01EF) == "Inherited"

    def test_get_script_past(self) -> None:
        assert get_script(0xE01F0) == "Unknown"
