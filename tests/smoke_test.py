from unittest import TestCase

from jkUnicode import UniInfo


class SmokeTest(TestCase):
    u = UniInfo(42)
    assert u.block == "Basic Latin"
