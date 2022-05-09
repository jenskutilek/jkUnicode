#!/usr/bin/env python3

import argparse
from jkUnicode import UniInfo


def uniinfo():
    parser = argparse.ArgumentParser(
        description="Show information about Unicode codepoints."
    )
    parser.add_argument(
        "codepoint", type=int, nargs="+", help="One or more Unicode codepoints"
    )

    args = parser.parse_args()
    ui = UniInfo()
    for uni in args.codepoint:
        ui.unicode = uni
        print(ui)
        print()


if __name__ == "__main__":
    uniinfo()
