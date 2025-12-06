import unittest

import pytest

from jkUnicode.tools.helpers import RangeDict


class TestRangeDict(unittest.TestCase):
    def test_existing_key(self):
        rd = RangeDict({(1, 10): "Foo", (12, 13): "Bar"})
        assert rd[1] == "Foo"

    def test_unknown_key(self):
        rd = RangeDict({(1, 10): "Foo", (12, 13): "Bar"})
        with pytest.raises(KeyError):
            _ = rd[0]

    def test_none_key(self):
        rd = RangeDict({(1, 10): "Foo", (12, 13): "Bar"})
        with pytest.raises(KeyError):
            _ = rd[None]
