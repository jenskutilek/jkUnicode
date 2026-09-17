import unittest

from jkUnicode.uniBlock import get_block, get_codepoints, get_codepoints_min_max


class TestUniScript(unittest.TestCase):
    def test_get_block_0x4ff(self) -> None:
        assert get_block(0x4FF) == "Cyrillic"

    def test_get_block_0x500(self) -> None:
        assert get_block(0x500) == "Cyrillic Supplement"

    def test_get_codepoints(self) -> None:
        # fmt: off
        assert get_codepoints("Cyrillic Supplement") == {
            1280, 1281, 1282, 1283, 1284, 1285, 1286, 1287, 1288, 1289, 1290, 1291,
            1292, 1293, 1294, 1295, 1296, 1297, 1298, 1299, 1300, 1301, 1302, 1303,
            1304, 1305, 1306, 1307, 1308, 1309, 1310, 1311, 1312, 1313, 1314, 1315,
            1316, 1317, 1318, 1319, 1320, 1321, 1322, 1323, 1324, 1325, 1326, 1327
        }
        # fmt: on

    def test_get_codepoints_min_max(self) -> None:
        assert get_codepoints_min_max("Cyrillic Supplement") == (1280, 1327)

    def test_get_codepoints_min_max_none(self) -> None:
        assert get_codepoints_min_max("This block doesn't exist") is None

    def test_get_codepoints_empty(self) -> None:
        assert get_codepoints("This block doesn't exist") == set()
