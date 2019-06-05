#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

import argparse
import codecs
import os
from os.path import exists, join
from string import strip

aglfnAdditions = {
    'NULL': 0x0000,
    'CR': 0xd,
    'twosuperior': 0x00B2,
    'threesuperior': 0x00B3,
    'onesuperior': 0x00B9,
    'fi': 0xfb01,
    'fl': 0xfb02,
}

module_path = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
data_path = os.path.join(module_path, "data")
gen_message = "# This is a generated file, use data-scripts/generatePyUniData.py to edit and regenerate.\n\n"


def write_names():
    # Unicode names
    print("Writing Unicode Character Names ...")
    src_file = join(data_path, "UnicodeData.txt")
    if exists(src_file):
        with codecs.open(
            os.path.join(module_path, "uniName.py"), 'w', encoding='utf-8'
        ) as outfile:
            outfile.write(gen_message)
            outfile.write("uniName = {")
            with codecs.open(src_file, encoding='utf-8') as f:
                for line in f:
                    elements = line.split(';')
                    outfile.write("\n    0x%s: '%s'," % (
                        elements[0], elements[1]
                    ))
            outfile.write("\n}")
        print("OK.")
    else:
        print("    WARNING: File UnicodeData.txt not found, Unicode name data not regenerated.")


def write_case_mappings():
    # Unicode names
    print("Writing Unicode Case Mappings ...")
    src_file = join(data_path, "UnicodeData.txt")
    if exists(src_file):
        with codecs.open(
            os.path.join(module_path, "uniCase.py"), 'w', encoding='utf-8'
        ) as outfile:
            outfile.write(gen_message)
            outfile.write("uniUpperCaseMapping = {")
            uc = []
            lc = []
            with codecs.open(src_file, encoding='utf-8') as f:
                for line in f:
                    elements = line.strip().split(';')

                    # Uppercase mapping
                    ucm = elements[14]
                    if ucm:
                        uc.append((elements[0], ucm))

                    # Lowercase mapping
                    lcm = elements[13]
                    if lcm:
                        lc.append((elements[0], lcm))
            for item in uc:
                outfile.write("\n    0x%s: 0x%s," % item)
            outfile.write("\n}\n\nuniLowerCaseMapping = {")
            for item in lc:
                outfile.write("\n    0x%s: 0x%s," % item)
            outfile.write("\n}\n")
        print("OK.")
    else:
        print("WARNING: File UnicodeData.txt not found, Unicode case mapping data not regenerated.")


def write_category():
    # Unicode category names
    print("Writing Unicode Categories ...")
    src_file = join(data_path, "UnicodeData.txt")
    if exists(src_file):
        with codecs.open(join(module_path, "uniCat.py"), 'w', encoding='utf-8') as outfile:
            outfile.write(gen_message)
            outfile.write("uniCat = {")
            with codecs.open(src_file, encoding='utf-8') as f:
                for line in f:
                    elements = line.split(';')
                    outfile.write("\n    0x%s: '%s'," % (
                        elements[0],
                        elements[2]
                    ))
            outfile.write("\n}")
        print("OK.")
    else:
        print("WARNING: File UnicodeData.txt not found, Unicode category data not regenerated.")

def write_blocks():
    # Unicode blocks
    print("Writing Unicode Blocks ...")
    src_file = join(data_path, "Blocks.txt")
    if exists(src_file):
        with codecs.open(
            os.path.join(module_path, "uniBlockData.py"), 'w', encoding='utf-8'
        ) as outfile:
            outfile.write(gen_message)
            outfile.write("uniBlocks = {")
            with codecs.open(src_file, encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if line.startswith("#"):
                        continue
                    if len(line.strip()) > 0:
                        elements = line.split('; ')
                        if len(elements) != 2:
                            print(
                                "ERROR in Line %i while splitting line: %s" % (
                                    i, elements
                                )
                            )
                            print("      %s" % line)
                        else:
                            c_range, name = elements
                            start_end = c_range.split("..")
                            if len(start_end) != 2:
                                print(
                                    "ERROR in Line %i while splitting range: %s" % (
                                        i, start_end
                                    )
                                )
                                print("      %s" % line)
                            else:
                                start = int(start_end[0], 16)
                                end   = int(start_end[1], 16)
                                outfile.write(
                                    "\n    (0x%04x, 0x%04x): '%s', # %i characters" % (
                                        start, end, name.strip(), end-start+1
                                    )
                                )
            outfile.write("\n}")
        print("OK.")
    else:
        print("WARNING: File Blocks.txt not found, Unicode block data not regenerated.")


def write_decomposition():
    # Unicode decomposition
    print("Writing Unicode Decomposition Mappings ...")
    src_file = join(data_path, "UnicodeData.txt")
    if exists(src_file):
        with codecs.open(
            os.path.join(module_path, "uniDecomposition.py"),
            'w',
            encoding='utf-8'
        ) as outfile:
            outfile.write(gen_message)
            outfile.write("uniDecompositionMapping = {")
            dc = []
            with codecs.open(src_file, encoding='utf-8') as f:
                for line in f:
                    elements = line.strip().split(';')

                    # Decomposition mapping
                    dcm = elements[5]
                    if dcm:
                        codes = dcm.split(" ")
                        if not codes[0].startswith("<"):
                            dc.append((elements[0], codes))

            for code, decomp_sequence in dc:
                outfile.write("\n    0x%s: [%s]," % (
                    code,
                    ", ".join([
                        "0x%s" % d
                        for d in decomp_sequence
                    ])
                ))
            outfile.write("\n}\n")
        print("OK.")
    else:
        print("WARNING: File UnicodeData.txt not found, Unicode name data not regenerated.")


def write_scripts():
    # Unicode scripts
    print("Writing Unicode Scripts ...")
    src_file = os.path.join(data_path, "Scripts.txt")
    if exists(src_file):
        with codecs.open(
            os.path.join(module_path, "uniScript.py"), 'w', encoding='utf-8'
        ) as outfile:
            outfile.write(gen_message)
            outfile.write("uniScript = {")
            with codecs.open(src_file, encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    elements = line.split(';')
                    rng = elements[0].strip()
                    script = elements[1].strip().split("#")[0].strip()
                    if ".." in rng:
                        start, end = rng.split("..")
                    else:
                        start = rng
                        end = rng
                    start = int(start, 16)
                    end = int(end, 16)
                    for code in range(start, end):
                        outfile.write("\n    0x%s: %s," % (code, script))
            outfile.write("\n}\n")
        print("OK.")
    else:
        print("WARNING: File Scripts.txt not found, Unicode script data not regenerated.")


def write_aglfn():
    # Adobe Glyph List for New Fonts
    print("Writing AGLFN data ...")
    src_file = os.path.join(data_path, "aglfn.txt")
    if exists(src_file):
        with codecs.open(
            os.path.join(module_path, "aglfnData.py"), 'w', encoding='utf-8'
        ) as outfile:
            outfile.write(gen_message)
            outfile.write("nameToUnicode = {")
            with codecs.open(src_file, encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if line[0] != "#":
                        elements = line.split(';')
                        if len(elements) != 3:
                            print("ERROR parsing line %i: %s" % (i, line))
                        else:
                            outfile.write("\n    '%s': 0x%s, # %s" % (
                                elements[1],
                                elements[0],
                                strip(elements[2])
                            ))
            if aglfnAdditions:
                outfile.write("\n    # Local additions:")
            for k in sorted(aglfnAdditions.keys()):
                outfile.write("\n    '%s': 0x%04x," % (k, aglfnAdditions[k]))
            outfile.write("\n}\n")
        print("OK.")
    else:
        print("WARNING: File aglfn.txt not found, AGLFN data not regenerated.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Regenerate Unicode and glyph name data."
    )
    parser.add_argument(
        '-a', '--aglfn',
        action="store_true", default=False,
        help='Regenerate glyph name data'
    )
    parser.add_argument(
        '-b', '--block',
        action="store_true", default=False,
        help='Regenerate Unicode block data'
    )
    parser.add_argument(
        '-c', '--case',
        action="store_true", default=False,
        help='Regenerate Unicode case mapping data'
    )
    parser.add_argument(
        '-d', '--decomposition',
        action="store_true", default=False,
        help='Regenerate Unicode decomposition data'
    )
    parser.add_argument(
        '-n', '--name',
        action="store_true", default=False,
        help='Regenerate Unicode name data'
    )
    parser.add_argument(
        '-t', '--category',
        action="store_true", default=False,
        help='Regenerate Unicode category data'
    )
    parser.add_argument(
        '-s', '--script',
        action="store_true", default=False,
        help='Regenerate Unicode script data'
    )
    args = parser.parse_args()
    if not any([
        args.aglfn,
        args.case,
        args.decomposition,
        args.name,
        args.category,
        args.script,
    ]):
        write_aglfn()
        write_blocks()
        write_case_mappings()
        write_decomposition()
        write_names()
        write_category()
        write_scripts()
    else:
        if args.aglfn:
            write_aglfn()
        if args.block:
            write_blocks()
        if args.case:
            write_case_mappings()
        if args.decomposition:
            write_decomposition()
        if args.name:
            write_names()
        if args.category:
            write_category()
        if args.script:
            write_scripts()
