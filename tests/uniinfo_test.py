import unittest
from jkUnicode import UniInfo


class TestUniInfo(unittest.TestCase):
    def test_caching_block(self):
        u = UniInfo(42)
        assert u.block == "Basic Latin"
        u.unicode = 4200
        assert u.block == "Myanmar"
        u.unicode = None
        assert u.block is None
