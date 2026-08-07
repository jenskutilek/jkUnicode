import jkUnicode.tools.helpers
from jkUnicode.uniScriptData import uniScripts

uniScriptToName = jkUnicode.tools.helpers.RangeDict(uniScripts)


def get_script(codepoint: int) -> str:
    try:
        return uniScriptToName[codepoint]
    except KeyError:
        return "Unknown"
