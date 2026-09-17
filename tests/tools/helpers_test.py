import unittest

import pytest

from jkUnicode.tools.helpers import RangeDict


class TestRangeDict(unittest.TestCase):
    def test_init_none(self) -> None:
        rd = RangeDict()
        assert isinstance(rd, RangeDict)

    def test_existing_key(self) -> None:
        rd = RangeDict({(1, 10): "Foo", (12, 13): "Bar"})
        assert rd[1] == "Foo"

    def test_unknown_key(self) -> None:
        rd = RangeDict({(1, 10): "Foo", (12, 13): "Bar"})
        with pytest.raises(KeyError):
            rd[0]

    def test_none_key(self) -> None:
        rd = RangeDict({(1, 10): "Foo", (12, 13): "Bar"})
        with pytest.raises(KeyError):
            rd[None]

    def test_setitem_key_reversed(self) -> None:
        with pytest.raises(RuntimeError):
            RangeDict({(2, 1): "Foo", (12, 13): "Bar"})

    def test_setitem_key_invalid(self) -> None:
        with pytest.raises(TypeError):
            RangeDict({1: "Foo", 2: "Bar"})

    def test_setitem_key_invalid_length(self) -> None:
        with pytest.raises(ValueError):
            RangeDict({(1, 2, 3): "Foo"})

    def test_contains_key(self) -> None:
        rd = RangeDict({(1, 10): "Foo", (12, 13): "Bar"})
        assert 2 in rd

    def test_contains_key_false(self) -> None:
        rd = RangeDict({(1, 10): "Foo", (12, 13): "Bar"})
        assert 15 not in rd
