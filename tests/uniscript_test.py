import unittest

from jkUnicode.uniScript import get_script


class TestUniScript(unittest.TestCase):
    def test_get_script_0x4ff(self):
        assert get_script(0x4FF) == "Cyrillic"

    def test_get_script_0x500(self):
        assert get_script(0x500) == "Cyrillic"
