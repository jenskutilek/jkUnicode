import jkUnicode.tools.helpers
from jkUnicode.uniCatData import uniCat

uniCatToName = jkUnicode.tools.helpers.RangeDict(uniCat)


def get_category(codepoint: int) -> str:
    try:
        return uniCatToName[codepoint]
    except KeyError:
        return "<undefined>"
