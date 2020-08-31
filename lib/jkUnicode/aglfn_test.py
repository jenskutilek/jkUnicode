import unittest
from .aglfn import getUnicodeForGlyphname


class TestAglfn(unittest.TestCase):
    def _check_dict(self, expected_results_dict):
        for key, value in expected_results_dict.items():
            self.assertEqual(getUnicodeForGlyphname(key), value)

    def test_list(self):
        self._check_dict(
            {
                "AEacute": 0x1FC,
                "Eta": 0x397,
                "union": 0x222A,
                "universal": 0x2200,
                "H18533": 0x25CF,
                "SF080000": 0x251C,
                "NULL": 0x0,
                "CR": 0xD,
                # "Scommaaccent": 0x218,
                # "afii61352": 0x2116,
            }
        )

    def test_uni_bmp(self):
        self._check_dict(
            {"union": 0x222A, "uni0162": 0x162}
        )

    def test_u(self):
        self._check_dict(
            {
                "u": 0x75,
                "uacute": 0xFA,
                "union": 0x222A,
                "universal": 0x2200,
                "u1F6AA": 0x1F6AA,
                "u0162": None,
                "u00162": 0x162,
                "ucaron": None,
            }
        )

    def test_ornaments(self):
        self._check_dict(
            {"orn000": 0xEA00, "orn999": 0xEA00 + 999}
        )

    def test_ligatures(self):
        self._check_dict(
            {"f_l": None, "uni0162_h": None}
        )


if __name__ == "__main__":
    unittest.main()
