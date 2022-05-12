import unittest
from jkUnicode.orthography import Orthography


class TestOrthography(unittest.TestCase):
    def test_instantiation_from_dict(self):
        ot = Orthography(
            info_obj=None,
            code="de",
            script="LATN",
            territory="DE",
            info_dict={
                "name": "Deutsch",
            },
        )
        assert ot.name == "Deutsch"
