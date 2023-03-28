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

    def test_caching_category(self):
        u = UniInfo(42)
        assert u.category == "Punctuation, Other"
        u.unicode = 4200
        assert u.category == "Mark, Spacing Combining"
        u.unicode = None
        assert u.category is None

    def test_caching_category_short(self):
        u = UniInfo(42)
        assert u.category_short == "Po"
        u.unicode = 4200
        assert u.category_short == "Mc"
        u.unicode = None
        assert u.category_short is None

    def test_caching_glyphname(self):
        u = UniInfo(ord("Ä"))
        assert u.glyphname == "Adieresis"
        u.unicode = ord("ẞ")
        assert u.glyphname == "uni1E9E"
        u.unicode = None
        assert u.glyphname is None

    def test_caching_decomposition_mapping(self):
        u = UniInfo(ord("Ä"))
        assert u.char == "Ä"
        assert u.decomposition_mapping == [0x41, 0x308]
        u.unicode = ord("ø")
        assert u.decomposition_mapping == []
        u.unicode = ord("ó")
        assert u.decomposition_mapping == [0x6F, 0x301]
        u.unicode = None
        assert u.decomposition_mapping == []

    def test_caching_lc_mapping(self):
        u = UniInfo(ord("Ä"))
        assert u.lc_mapping == 0xE4
        u.unicode = ord("Ü")
        assert u.lc_mapping == 0xFC
        u.unicode = None
        assert u.lc_mapping is None

    def test_caching_name(self):
        u = UniInfo(ord("Ä"))
        assert u.name == "LATIN CAPITAL LETTER A WITH DIAERESIS"
        u.unicode = ord("Ü")
        assert u.name == "LATIN CAPITAL LETTER U WITH DIAERESIS"
        u.unicode = None
        assert u.name is None

    def test_caching_nice_name(self):
        u = UniInfo(ord("Ä"))
        assert u.nice_name == "Latin capital letter A with diaeresis"
        u.unicode = ord("Ü")
        assert u.nice_name == "Latin capital letter U with diaeresis"
        u.unicode = None
        assert u.nice_name is None

    def test_caching_script(self):
        u = UniInfo(ord("ä"))
        assert u.script == "Latin"
        u.unicode = ord("π")
        assert u.script == "Greek"
        u.unicode = None
        assert u.script is None

    def test_caching_uc_mapping(self):
        u = UniInfo(ord("ä"))
        assert u.uc_mapping == 0xC4
        u.unicode = ord("ü")
        assert u.uc_mapping == 0xDC
        u.unicode = None
        assert u.uc_mapping is None

    def test_char(self):
        u = UniInfo(ord("Ä"))
        assert u.char == "Ä"
        u.unicode = 0x1E9E
        assert u.char == "ẞ"
        u.unicode = None
        assert u.char is None

    def test_char_setter(self):
        u = UniInfo(ord("Ä"))
        assert u.char == "Ä"
        u.char = "ẞ"
        assert u.unicode == 0x1E9E
        u.char = None
        assert u.unicode is None
