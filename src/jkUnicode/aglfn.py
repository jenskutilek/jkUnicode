from re import compile

from jkUnicode.aglfnData import nameToUnicode

# Build reverse dictionary
unicodeToName = {value: key for key, value in nameToUnicode.items()}


def getUnicodeForGlyphname(name: str) -> int | None:
    """
    Return the Unicode value as integer or None that is assigned to the specified glyph
    name. It handles AGLFN names, uniXXXX names, uXXXXX names, ligature names, variant
    names, and PUA-encoded ornament names (orn001 - orn999, starting at 0xEA01).

    Args:
        name (str): The glyph name.

    Returns:
        int | None: The codepoint, or None if the glyph name refers to an unencoded
            glyph.
    """
    ornName = compile("^orn[0-9]{3}$")
    length = len(name)
    if "_" in name or "." in name[1:]:
        return None
    elif name in nameToUnicode:
        return nameToUnicode[name]
    elif length == 7 and name.startswith("uni"):
        return int(name[3:], 16)
    elif length == 6 and name.startswith("u"):
        try:
            return int(name[1:], 16)
        except ValueError:
            return None
    elif ornName.match(name):
        return 0xEA00 + int(name[3:6])
    else:
        return None


def getGlyphnameForUnicode(code: int | None) -> str | None:
    """
    Return the AGLFN glyph name for the specified Unicode codepoint.

    Args:
        code (int | None): The codepoint.

    Returns:
        str | None: The glyph name for the codepoint, or None if the codepoint is None.
    """
    if code is None:
        return None
    elif code in unicodeToName:
        return unicodeToName[code]
    elif code < 0xFFFF:
        return f"uni{code:04X}"
    else:
        return f"u{code:05X}"
