import unittest

import pytest

from jkUnicode.tools.xmlhelpers import filtered_char_list


class XMLHelpersTest(unittest.TestCase):
    def test_filtered_char_list(self) -> None:
        input = (
            "[\\u200C\\u200D-\\u200F A {A\\u0301} {E \\u0302} {ij} {a b c} 未-札 \\]]"
        )
        output = [
            "A",
            "E",
            "]",
            "a",
            "b",
            "c",
            "i",
            "j",
            "\u0301",
            "\u0302",
            "\u200c",
            "\u200d",
            "\u200e",
            "\u200f",
            "\u672a",
            "\u672b",
            "\u672c",
            "\u672d",
        ]
        assert filtered_char_list(input, True) == output


# (u"[á à ã {ą\\u0301} {ą\\u0303} {ch} {dz} {dž} é è ẽ {ę\\u0301} {ę\\u0303} {ė\\u0301} {ė\\u0303} {i\\u0307\\u0301}í {i\\u0307\\u0300}ì {i\\u0307\\u0303}ĩ {į\\u0301}{į\\u0307\\u0301} {į\\u0303}{į\\u0307\\u0303} {j\\u0303}{j\\u0307\\u0303} {l\\u0303} {m\\u0303} ñ ó ò õ q {r\\u0303} ú ù ũ {ų\\u0301} {ų\\u0303} {ū\\u0301} {ū\\u0303} w x]", [u'c', u'd', u'h', u'i', u'j', u'l', u'm', u'q', u'r', u'w', u'x', u'z', u'\xe0', u'\xe1', u'\xe3', u'\xe8', u'\xe9', u'\xec', u'\xed', u'\xf1', u'\xf2', u'\xf3', u'\xf5', u'\xf9', u'\xfa', u'\u0105', u'\u0117', u'\u0119', u'\u0129', u'\u012f', u'\u0169', u'\u016b', u'\u0173', u'\u017e', u'\u0300', u'\u0301', u'\u0303', u'\u0307', u'\u1ebd'])  # noqa: E501
# u"[a á à â ǎ ā {a\\u1DC6}{a\\u1DC7} b ɓ c d e é è ê ě ē {e\\u1DC6}{e\\u1DC7} ɛ {ɛ\\u0301} {ɛ\\u0300} {ɛ\\u0302} {ɛ\\u030C} {ɛ\\u0304} {ɛ\\u1DC6}{ɛ\\u1DC7} f g h i í ì î ǐ ī {i\\u1DC6}{i\\u1DC7} j k l m n ń ǹ ŋ o ó ò ô ǒ ō {o\\u1DC6}{o\\u1DC7} ɔ {ɔ\\u0301} {ɔ\\u0300} {ɔ\\u0302} {ɔ\\u030C} {ɔ\\u0304} {ɔ\\u1DC6}{ɔ\\u1DC7} p r s t u ú ù û ǔ ū {u\\u1DC6}{u\\u1DC7} v w y z]"  # noqa: E501
# u"[\\u0F7E ཿ ཀ {ཀ\\u0FB5} \\u0F90 {\\u0F90\\u0FB5} ཁ \\u0F91 ག {ག\\u0FB7} \\u0F92 {\\u0F92\\u0FB7} ང \\u0F94 ཅ \\u0F95 ཆ \\u0F96 ཇ \\u0F97 ཉ \\u0F99 ཊ \\u0F9A ཋ \\u0F9B ཌ {ཌ\\u0FB7} \\u0F9C {\\u0F9C\\u0FB7} ཎ \\u0F9E ཏ \\u0F9F ཐ \\u0FA0 ད {ད\\u0FB7} \\u0FA1 {\\u0FA1\\u0FB7} ན \\u0FA3 པ \\u0FA4 ཕ \\u0FA5 བ {བ\\u0FB7} \\u0FA6 {\\u0FA6\\u0FB7} མ \\u0FA8 ཙ \\u0FA9 ཚ \\u0FAA ཛ {ཛ\\u0FB7} \\u0FAB {\\u0FAB\\u0FB7} ཝ \\u0FAD \\u0FBA ཞ \\u0FAE ཟ \\u0FAF འ \\u0FB0 ཡ \\u0FB1 \\u0FBB ར ཪ \\u0FB2 \\u0FBC ལ \\u0FB3 ཤ \\u0FB4 ཥ \\u0FB5 ས \\u0FB6 ཧ \\u0FB7 ཨ \\u0FB8 \\u0F72 {\\u0F71\\u0F72} \\u0F80 {\\u0F71\\u0F80} \\,  # noqa: E501
# u"未-札"
