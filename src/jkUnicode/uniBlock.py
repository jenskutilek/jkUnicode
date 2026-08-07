import jkUnicode.tools.helpers
from jkUnicode.uniBlockData import uniBlocks

uniBlockToName = jkUnicode.tools.helpers.RangeDict(uniBlocks)

# The reverse mapping of names to blocks
uniNameToBlock = {}
for k, v in uniBlockToName.items():
    if v not in uniNameToBlock:
        uniNameToBlock[v] = k
    else:
        print(f"ERROR: Duplicate block name: {v}")


def get_block(codepoint) -> str | None:
    try:
        return uniBlockToName[codepoint]
    except KeyError:
        return None


def get_codepoints_min_max(block_name) -> tuple[int, int] | None:
    try:
        return uniNameToBlock[block_name]
    except KeyError:
        return None


def get_codepoints(block_name) -> set[int]:
    try:
        low, high = uniNameToBlock[block_name]
        return set(range(low, high + 1))
    except KeyError:
        return set()
