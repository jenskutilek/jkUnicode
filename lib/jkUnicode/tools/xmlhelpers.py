# The dirty hacky stuff is outsourced into this file

from re import compile
from jkUnicode import getUnicodeChar

from typing import Any, List

# Regex to match unicode sequences, e.g. \u0302
unicode_seq = compile("^u([0-9A-F]+)")


class Buffer:
    def __init__(self, string: str = "") -> None:
        self._str = string

    def add(self, value: str) -> None:
        self._str += value

    def clear(self) -> None:
        self._str = ""

    def flush(self) -> str:
        v = self.__get__()
        self.clear()
        return v

    def __get__(self) -> str:
        m = unicode_seq.search(self._str)
        if m is None:
            return self._str

        group = str(m.groups(0)[0])
        return getUnicodeChar(int(group, 16))

    def __repr__(self) -> str:
        return self._str


class FilteredList:
    def __init__(self) -> None:
        self._value: List[Any] = []

    def add(self, value: Any) -> None:
        if value:
            self._value.append(value)

    def get(self) -> Any:
        return self._value

    def __repr__(self) -> str:
        return str(self._value)


def filtered_char_list(xml_char_list: str, debug: bool = False) -> List[str]:
    # Filter backslashes and other peculiarities of the XML format from the
    # character list
    if xml_char_list[0] == "[" and xml_char_list[-1] == "]":
        xml_char_list = xml_char_list[1:-1]
    else:
        print("ERROR: Character list string from XML was not wrapped in [].")
        return []

    filtered = FilteredList()
    in_escape = False
    in_uniesc = False
    buf = Buffer()

    for c in xml_char_list:
        if debug:
            print("Chunk: '%s', buffer:'%s'" % (c, buf))
        if in_uniesc:
            if c in "\\}{- ":
                filtered.add(buf.flush())
                in_uniesc = False
                if c == "\\":
                    in_escape = True
                else:
                    in_escape = False
                    if c == "-":
                        filtered.add("RANGE")
            else:
                buf.add(c)
        else:
            if c == "\\":
                if in_escape:
                    filtered.add(buf.flush())
                    filtered.add(c)
                else:
                    in_escape = True
            elif c == "}":
                if in_escape:
                    filtered.add(buf.flush())
                    filtered.add(c)
                    in_escape = False
            elif c == "{":
                if in_escape:
                    filtered.add(c)
                    in_escape = False
            elif c == " ":
                filtered.add(buf.flush())
                in_escape = False
            elif c == "-":
                if in_escape:
                    filtered.add(buf.flush())
                    filtered.add(c)
                    in_escape = False
                else:
                    filtered.add("RANGE")
            elif c == "u":
                if in_escape:
                    in_uniesc = True
                    buf.add(c)
                else:
                    filtered.add(c)
            else:
                if c == u"\u2010":
                    c = "-"  # Replace proper hyphen by hyphen-minus
                if in_escape:
                    in_escape = False
                filtered.add(c)
                buf.clear()
            if debug:
                print("New buffer: '%s'" % buf)

    filtered.add(buf.flush())

    result = filtered.get()

    # Expand ranges
    final = []
    f: str
    for i, f in enumerate(result):
        if f == "RANGE":
            start = ord(result[i - 1]) + 1
            end = ord(result[i + 1])
            # print("RANGE: %04X, %04X" % (start, end))
            for g in range(start, end):
                # print("0x%04X" % g)
                final.append(chr(g))
        else:
            final.append(f)

    if debug:
        print(final)
    return sorted(list(set(final)))


if __name__ == "__main__":
    lists = [
        (
            u"[\\u200C\\u200D-\\u200F A {A\\u0301} {E \\u0302} {ij} {a b c} ???-??? \\]]",
            [
                u"A",
                u"E",
                u"]",
                u"a",
                u"b",
                u"c",
                u"i",
                u"j",
                u"\u0301",
                u"\u0302",
                u"\u200c",
                u"\u200d",
                u"\u200e",
                u"\u200f",
                u"\u672a",
                u"\u672b",
                u"\u672c",
                u"\u672d",
            ],
        )
        # (u"[?? ?? ?? {??\\u0301} {??\\u0303} {ch} {dz} {d??} ?? ?? ??? {??\\u0301} {??\\u0303} {??\\u0301} {??\\u0303} {i\\u0307\\u0301}?? {i\\u0307\\u0300}?? {i\\u0307\\u0303}?? {??\\u0301}{??\\u0307\\u0301} {??\\u0303}{??\\u0307\\u0303} {j\\u0303}{j\\u0307\\u0303} {l\\u0303} {m\\u0303} ?? ?? ?? ?? q {r\\u0303} ?? ?? ?? {??\\u0301} {??\\u0303} {??\\u0301} {??\\u0303} w x]", [u'c', u'd', u'h', u'i', u'j', u'l', u'm', u'q', u'r', u'w', u'x', u'z', u'\xe0', u'\xe1', u'\xe3', u'\xe8', u'\xe9', u'\xec', u'\xed', u'\xf1', u'\xf2', u'\xf3', u'\xf5', u'\xf9', u'\xfa', u'\u0105', u'\u0117', u'\u0119', u'\u0129', u'\u012f', u'\u0169', u'\u016b', u'\u0173', u'\u017e', u'\u0300', u'\u0301', u'\u0303', u'\u0307', u'\u1ebd'])
        # u"[a ?? ?? ?? ?? ?? {a\\u1DC6}{a\\u1DC7} b ?? c d e ?? ?? ?? ?? ?? {e\\u1DC6}{e\\u1DC7} ?? {??\\u0301} {??\\u0300} {??\\u0302} {??\\u030C} {??\\u0304} {??\\u1DC6}{??\\u1DC7} f g h i ?? ?? ?? ?? ?? {i\\u1DC6}{i\\u1DC7} j k l m n ?? ?? ?? o ?? ?? ?? ?? ?? {o\\u1DC6}{o\\u1DC7} ?? {??\\u0301} {??\\u0300} {??\\u0302} {??\\u030C} {??\\u0304} {??\\u1DC6}{??\\u1DC7} p r s t u ?? ?? ?? ?? ?? {u\\u1DC6}{u\\u1DC7} v w y z]"
        # u"[\\u0F7E ??? ??? {???\\u0FB5} \\u0F90 {\\u0F90\\u0FB5} ??? \\u0F91 ??? {???\\u0FB7} \\u0F92 {\\u0F92\\u0FB7} ??? \\u0F94 ??? \\u0F95 ??? \\u0F96 ??? \\u0F97 ??? \\u0F99 ??? \\u0F9A ??? \\u0F9B ??? {???\\u0FB7} \\u0F9C {\\u0F9C\\u0FB7} ??? \\u0F9E ??? \\u0F9F ??? \\u0FA0 ??? {???\\u0FB7} \\u0FA1 {\\u0FA1\\u0FB7} ??? \\u0FA3 ??? \\u0FA4 ??? \\u0FA5 ??? {???\\u0FB7} \\u0FA6 {\\u0FA6\\u0FB7} ??? \\u0FA8 ??? \\u0FA9 ??? \\u0FAA ??? {???\\u0FB7} \\u0FAB {\\u0FAB\\u0FB7} ??? \\u0FAD \\u0FBA ??? \\u0FAE ??? \\u0FAF ??? \\u0FB0 ??? \\u0FB1 \\u0FBB ??? ??? \\u0FB2 \\u0FBC ??? \\u0FB3 ??? \\u0FB4 ??? \\u0FB5 ??? \\u0FB6 ??? \\u0FB7 ??? \\u0FB8 \\u0F72 {\\u0F71\\u0F72} \\u0F80 {\\u0F71\\u0F80} \\,
        # u"???-???"
    ]

    for cl, r in lists:
        ll = filtered_char_list(cl, True)
        print("Result:", ll)
        if ll == r:
            print("OK")
        else:
            print("ERROR")
