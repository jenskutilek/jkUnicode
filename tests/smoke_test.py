from unittest import TestCase

from jkUnicode import UniInfo


class SmokeTest(TestCase):
    def test_minimal(self) -> None:
        u = UniInfo(42)
        assert u.block == "Basic Latin"
