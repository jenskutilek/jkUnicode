import unittest

from jkUnicode.uniNiceName import (
    get_nice_name,
    transform_allah,
    transform_capital_letter,
    transform_small_letter,
)


class TestUniNiceName(unittest.TestCase):
    def test_get_nice_name_allah_none(self) -> None:
        assert get_nice_name("AKBAR ISOLATED FORM") == "Akbar isolated form"

    def test_transform_allah_none(self) -> None:
        assert not transform_allah("AKBAR ISOLATED FORM")

    def test_get_nice_name_allah_start(self) -> None:
        assert get_nice_name("ALLAH ISOLATED FORM") == "Allah isolated form"

    def test_transform_allah_start(self) -> None:
        assert not transform_allah("ALLAH ISOLATED FORM")

    def test_transform_allah_mid(self) -> None:
        assert (
            transform_allah("ARABIC SIGN RADI ALLAHOU ANHU")
            == "Arabic sign radi Allahou anhu"
        )

    def test_get_nice_name_allah_mid(self) -> None:
        assert (
            get_nice_name("ARABIC SIGN RADI ALLAHOU ANHU")
            == "Arabic sign radi Allahou anhu"
        )

    def test_transform_allah_in_word(self) -> None:
        assert not transform_allah("SALLALLAHOU ALAYHE WASALLAM")

    def test_get_nice_name_allah_in_word(self) -> None:
        assert (
            get_nice_name("SALLALLAHOU ALAYHE WASALLAM")
            == "Sallallahou alayhe wasallam"
        )

    def test_transform_small_letter_fullwidth(self) -> None:
        assert (
            transform_small_letter("FULLWIDTH LATIN SMALL LETTER A")
            == "Fullwidth latin small letter a"
        )

    def test_transform_small_letter_latin(self) -> None:
        assert (
            transform_small_letter("FULLWIDTH LATIN SMALL LETTER A")
            == "Fullwidth latin small letter a"
        )

    def test_get_nice_name_small_letter_latin_single(self) -> None:
        assert get_nice_name("LATIN SMALL LETTER A") == "Latin small letter a"

    def test_get_nice_name_small_letter_latin_multi(self) -> None:
        assert get_nice_name("LATIN SMALL LETTER AE") == "Latin small letter ae"

    def test_get_nice_name_small_letter_greek_multi_space(self) -> None:
        assert (
            get_nice_name("GREEK SMALL LETTER FINAL SIGMA")
            == "Greek small letter final sigma"
        )

    def test_get_nice_name_small_letter_greek_multi_with(self) -> None:
        assert (
            get_nice_name("GREEK SMALL LETTER UPSILON WITH DIALYTIKA")
            == "Greek small letter upsilon with dialytika"
        )

    def test_transform_small_letter_ukrainian(self) -> None:
        assert (
            transform_small_letter(
                "CYRILLIC SUBSCRIPT SMALL LETTER BYELORUSSIAN-UKRAINIAN I"
            )
            == "Cyrillic subscript small letter Byelorussian-Ukrainian i"
        )

    def test_get_nice_name_small_letter_ukrainian_multi(self) -> None:
        assert (
            get_nice_name("CYRILLIC SMALL LETTER UKRAINIAN IE")
            == "Cyrillic small letter Ukrainian ie"
        )

    def test_transform_capital_letter_deseret_1(self) -> None:
        assert (
            transform_capital_letter("DESERET CAPITAL LETTER LONG AH")
            == "Deseret capital letter long Ah"
        )

    def test_transform_capital_letter_deseret_2(self) -> None:
        assert (
            transform_capital_letter("DESERET CAPITAL LETTER SHORT OO")
            == "Deseret capital letter short Oo"
        )

    def test_transform_capital_letter_ukrainian(self) -> None:
        assert (
            transform_capital_letter("CYRILLIC CAPITAL LETTER UKRAINIAN IE")
            == "Cyrillic capital letter Ukrainian Ie"
        )
