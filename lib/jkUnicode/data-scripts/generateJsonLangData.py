#!/usr/bin/env python3
from __future__ import annotations

import codecs
import copy
import os
import re
import xml.etree.ElementTree as ET

from jkUnicode.tools.xmlhelpers import filtered_char_list
from jkUnicode.aglfn import getGlyphnameForUnicode
from jkUnicode.tools.jsonhelpers import json_to_file, clean_json_dir
from pathlib import Path
from typing import Dict, List, Tuple, TypeAlias
from zipfile import ZipFile


CharDict: TypeAlias = Dict[str, List[int]]

LanguageCharsDict: TypeAlias = Dict[
    str, Dict[str, Dict[str, Dict[str, CharDict | str]]]
]


# FIXME
base_path = Path(os.path.split(Path(__file__).resolve().parent)[0])

# Input path for the CLDR zip file
zip_path = base_path / "data" / "core.zip"

# Input path for BCP47 language subtag data
tags_path = base_path / "data" / "language-subtag-registry"

# Output path for JSON files
json_path = base_path / "json"

# Path inside the zip file
xml_re = re.compile(r"^common/main/.+\.xml$")
en_path = "common/main/en.xml"


def extract_dict(root, key):
    elements = root.findall(key)
    d = {e.attrib["type"]: e.text for e in elements}
    return d


def extract_char_dict(root, key):
    elements = root.findall(key)
    d = {e.attrib["type"]: e.text for e in elements}
    return d


def format_char_list(char_list):
    return [
        "0x%04X %s %s" % (ord(cc), cc, getGlyphnameForUnicode(ord(cc)))
        for cc in char_list
    ]


def generate_language_tags(data_path: Path) -> None:
    if not data_path.exists():
        print(
            "File with language subtag data not found.\nPlease use the shell "
            f"script 'updateLangData.sh' to download '{data_path.name}'."
        )
        return

    with codecs.open(str(data_path), "rb", "utf-8") as f:
        _ = f.readline()
        lines = f.readlines()

    lines = unbreak_lines(lines)
    languages = []
    lang: Dict[str, str] | None = None
    for line in lines:
        line = line.strip()
        if line == "%%":
            if lang is not None:
                languages.append(lang)
            lang = {}
        else:
            parts = line.split(":", 1)
            assert len(parts) == 2
            key, value = parts
            assert lang is not None
            lang[key] = value.strip()
    from pprint import pprint

    pprint(languages)


def unbreak_lines(lines: List[str]) -> List[str]:
    # Remove continued lines (marked by two spaces at the beginning)
    long_lines: List[str] = []
    line_buffer = ""
    for line in lines:
        if line.startswith("  "):
            line_buffer += " " + line.strip()
        else:
            if line_buffer:
                long_lines.append(line_buffer)
            line_buffer = line
    if line_buffer:
        long_lines.append(line_buffer)
    return long_lines


def generate_language_data(zip_path: Path) -> None:

    if not zip_path.exists():
        print(
            "Zip file with XML data not found.\nPlease use the shell script "
            "'updateLangData.sh' to download it."
        )
        return

    with ZipFile(zip_path, "r") as z:
        names = z.namelist()
        if en_path not in names:
            print("'%s' not found in zip file." % en_path)
            return

        with z.open(en_path) as en_xml:

            # Extract language, script and territory names from the English data file

            root = ET.parse(en_xml).getroot()

            # Language names

            language_dict = extract_dict(
                root, "localeDisplayNames/languages/language"
            )
            try:
                # Root is not a language, but the template file
                del language_dict["root"]
            except KeyError:
                pass
            print("OK: Read %i language names." % len(language_dict))

            # Script names

            script_dict = extract_dict(
                root, "localeDisplayNames/scripts/script"
            )
            print("OK: Read %i script names." % len(script_dict))

            json_to_file(json_path, "scripts", script_dict)

            # Territory names

            territory_dict = extract_dict(
                root, "localeDisplayNames/territories/territory"
            )
            print("OK: Read %i territory names." % len(territory_dict))

            json_to_file(json_path, "territories", territory_dict)

        # Now parse all the separate language XML files

        print("Parsing language character data ...")
        language_chars, ignored_languages = parse_lang_char_data(
            z, language_dict, script_dict, territory_dict
        )

        for code in ignored_languages:
            del language_dict[code]

        sep_path = json_path / "languages"

        clean_json_dir(sep_path)

        json_to_file(json_path, "languages", language_dict)
        json_to_file(json_path, "ignored", ignored_languages)
        for code, v in language_chars.items():
            # print("json_to_file:", "%s" % code)
            json_to_file(sep_path, "%s" % code, v)


def extract_lang_code(internal_path: str, root) -> str | None:
    # Extract code
    code = root.findall("identity/language")
    if len(code) == 0:
        print("ERROR: Language code not found in file '%s'" % internal_path)
        return None
    elif len(code) == 1:
        return code[0].attrib["type"]
    else:
        print("ERROR: Language code ambiguous in file '%s'" % internal_path)
    return None


def extract_script_code(internal_path, root) -> str | None:
    # Extract script
    script = root.findall("identity/script")
    if len(script) == 0:
        # print("WARNING: Script not found in file '%s'" % internal_path)
        return "DFLT"
    elif len(script) == 1:
        return script[0].attrib["type"]
    else:
        print("ERROR: Script ambiguous in file '%s'" % internal_path)
    return None


def extract_territory_code(internal_path, root) -> str | None:
    # Extract territory
    territory = root.findall("identity/territory")
    if len(territory) == 0:
        # print("WARNING: Territory not found in file '%s'" % internal_path)
        return "dflt"
    elif len(territory) == 1:
        return territory[0].attrib["type"]
    else:
        print("ERROR: Territory ambiguous in file '%s'" % internal_path)
    return None


def extract_characters(root) -> Dict[str, List[int]]:
    # Extract characters
    char_dict = {}
    ec = root.findall("characters/exemplarCharacters")
    for c in ec:
        if "type" not in c.attrib:
            # Main entry
            u_list = format_char_list(filtered_char_list(c.text))
            if u_list:
                char_dict["base"] = u_list
        elif "type" in c.attrib:
            t = c.attrib["type"]
            if t in ["auxiliary", "punctuation"]:
                if t == "auxiliary":
                    t = "optional"
                u_list = format_char_list(filtered_char_list(c.text))
                if u_list:
                    char_dict[t] = u_list
    return char_dict


def parse_lang_char_data(
    z, language_dict, script_dict, territory_dict
) -> Tuple[LanguageCharsDict, List[str]]:
    language_chars: LanguageCharsDict = {}
    ignored_languages = copy.deepcopy(language_dict)

    i = 0

    for internal_path in z.namelist():
        if not xml_re.search(internal_path):
            continue

        with z.open(internal_path) as lang_xml:
            i += 1

            root = ET.parse(lang_xml).getroot()
            # print("File:", internal_path)

            code = extract_lang_code(internal_path, root)
            script = extract_script_code(internal_path, root)
            territory = extract_territory_code(internal_path, root)

            char_dict = extract_characters(root)

            if not char_dict:
                # print(
                #     "    XML for %s (%s/%s/%s) contains no character information"
                #     % (language_dict[code], script, code, territory)
                # )
                continue

            if code not in language_dict:
                if code != "root":
                    print(f"Language is not in master list: {code}")
                continue

            # print("Add information for", code)
            if code not in language_chars:
                # print("    Add entry for code to master dict:", code)
                assert code is not None
                language_chars[code] = {}

            if script not in language_chars[code]:
                # print("    Add entry for script/code to master dict:", script)
                assert script is not None
                language_chars[code][script] = {}

            # Found best matching entry from language_dict
            c_t_key = "%s_%s" % (code, territory)
            c_s_key = "%s_%s" % (code, script)
            all_key = "%s_%s_%s" % (code, script, territory)
            found = False
            name = "Unknown"
            for key in [all_key, c_t_key, c_s_key, code]:
                if key in language_dict:
                    found = True
                    name = language_dict[key]
                    try:
                        del ignored_languages[key]
                    except KeyError:
                        pass
                    break
            if not found:
                print(
                    "Could not determine name for %s/%s/%s"
                    % (script, code, territory)
                )

            # Build name including script or territory
            if script == "DFLT":
                if territory != "dflt":
                    name += " (%s)" % (
                        territory_dict[territory]
                        if territory in territory_dict
                        else territory,
                    )
            else:
                if territory == "dflt":
                    name += " (%s)" % (
                        script_dict[script]
                        if script in script_dict
                        else script,
                    )
                else:
                    name += " (%s, %s)" % (
                        script_dict[script]
                        if script in script_dict
                        else script,
                        territory_dict[territory]
                        if territory in territory_dict
                        else territory,
                    )

            assert territory is not None
            language_chars[code][script][territory] = {
                "name": name,
                "unicodes": char_dict,
            }
            # if territory in territory_dict:
            #   language_chars[code][script][territory]["territory"] = territory_dict[territory]

    print(f"Parsed {i} files.")
    return language_chars, ignored_languages


if __name__ == "__main__":
    generate_language_tags(tags_path)
    generate_language_data(zip_path)
