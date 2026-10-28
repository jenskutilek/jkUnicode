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


def get_block(codepoint: int | None) -> str | None:
    if codepoint is None:
        return None
    return uniBlockToName.get(codepoint)


def get_codepoints_min_max(block_name: str) -> tuple[int, int] | None:
    return uniNameToBlock.get(block_name)


def get_codepoints(block_name: str) -> set[int]:
    try:
        low, high = uniNameToBlock[block_name]
        return set(range(low, high + 1))
    except KeyError:
        return set()
