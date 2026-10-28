import jkUnicode.tools.helpers
from jkUnicode.uniScriptData import uniScripts

uniScriptToName = jkUnicode.tools.helpers.RangeDict(uniScripts)


def get_script(codepoint: int | None) -> str | None:
    if codepoint is None:
        return None
    try:
        return uniScriptToName[codepoint]
    except KeyError:
        return "Unknown"
