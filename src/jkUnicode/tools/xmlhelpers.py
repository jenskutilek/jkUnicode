# The dirty hacky stuff is outsourced into this file

from re import compile
from typing import Any

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
        return chr(int(group, 16))

    def __repr__(self) -> str:
        return self._str


class FilteredList:
    def __init__(self) -> None:
        self._value: list[Any] = []

    def add(self, value: Any) -> None:
        if value:
            self._value.append(value)

    def get(self) -> Any:
        return self._value

    def __repr__(self) -> str:
        return str(self._value)


def unescape_char_list(xml_char_list: str):
    filtered = FilteredList()
    in_escape = False
    in_uniesc = False
    buf = Buffer()

    for c in xml_char_list:
        # if debug:
        #     print("Chunk: '%s', buffer:'%s'" % (c, buf))
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
                if c == "\u2010":
                    c = "-"  # Replace proper hyphen by hyphen-minus
                if in_escape:
                    in_escape = False
                filtered.add(c)
                buf.clear()
            # if debug:
            #     print("New buffer: '%s'" % buf)

    filtered.add(buf.flush())

    return filtered.get()


def filtered_char_list(xml_char_list: str, debug: bool = False) -> list[str]:
    # Filter backslashes and other peculiarities of the XML format from the
    # character list
    if xml_char_list[0] == "[" and xml_char_list[-1] == "]":
        xml_char_list = xml_char_list[1:-1]
    else:
        print("ERROR: Character list string from XML was not wrapped in [].")
        return []

    result = unescape_char_list(xml_char_list)

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
    return sorted(set(final))
