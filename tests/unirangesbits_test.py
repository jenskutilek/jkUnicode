import unittest

from jkUnicode.uniRangesBits import getNameForRangeBit, getUnicodesForRangeBit


class TestUniRangesBits(unittest.TestCase):
    def test_getUnicodesForRangeBit_1(self):
        codes = getUnicodesForRangeBit(1)
        assert codes == list(range(0x80, 0x100))

    def test_getNameForRangeBit_1(self):
        assert getNameForRangeBit(1) == "Latin-1 Supplement"
