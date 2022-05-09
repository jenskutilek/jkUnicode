#!/usr/bin/env python3

import copy, os, re
import xml.etree.ElementTree as ET
from zipfile import ZipFile
from jkUnicode.tools.xmlhelpers import filtered_char_list
from jkUnicode.aglfn import getGlyphnameForUnicode
from jkUnicode.tools.jsonhelpers import json_to_file, clean_json_dir


base_path = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

# Input path for the CLDR zip file
zip_path = os.path.join(base_path, "data", "core.zip")

# Output path for JSON files
json_path = os.path.join(base_path, "json")

# Path inside the zip file
xml_re = re.compile("^common/main/.+\.xml$")
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


def generate_language_data(zip_path):

    if not (os.path.exists(zip_path)):
        print(
            "Zip file with XML data not found.\nPlease use the shell script "
            "'updateLangData.sh' to download it."
        )
        return False

    with ZipFile(zip_path, "r") as z:
        names = z.namelist()
        if not en_path in names:
            print("'%s' not found in zip file." % en_path)
            return False
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
            except:
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

        language_chars = {}
        ignored_languages = copy.deepcopy(language_dict)

        sep_path = os.path.join(json_path, "languages")

        i = 0

        for internal_path in z.namelist():
            if xml_re.search(internal_path):
                with z.open(internal_path) as lang_xml:

                    char_dict = {}
                    i += 1
                    root = ET.parse(lang_xml).getroot()
                    # print("File:", internal_path)

                    # Extract code
                    code = root.findall("identity/language")
                    if len(code) == 0:
                        print(
                            "ERROR: Language code not found in file '%s'"
                            % internal_path
                        )
                        code = None
                    elif len(code) == 1:
                        code = code[0].attrib["type"]
                    else:
                        print(
                            "ERROR: Language code ambiguous in file '%s'"
                            % internal_path
                        )
                        code = None
                    # print("    Code:", code)

                    # Extract script
                    script = root.findall("identity/script")
                    if len(script) == 0:
                        # print("WARNING: Script not found in file '%s'" % internal_path)
                        script = "DFLT"
                    elif len(script) == 1:
                        script = script[0].attrib["type"]
                    else:
                        print(
                            "ERROR: Script ambiguous in file '%s'"
                            % internal_path
                        )
                        script = None
                    # print("    Script:", script)

                    # Extract territory
                    territory = root.findall("identity/territory")
                    if len(territory) == 0:
                        # print("WARNING: Territory not found in file '%s'" % internal_path)
                        territory = "dflt"
                    elif len(territory) == 1:
                        territory = territory[0].attrib["type"]
                    else:
                        print(
                            "ERROR: Territory ambiguous in file '%s'"
                            % internal_path
                        )
                        territory = None
                    # print("    Territory:", territory)

                    # Extract characters
                    ec = root.findall("characters/exemplarCharacters")
                    for c in ec:
                        if "type" not in c.attrib:
                            # Main entry
                            u_list = format_char_list(
                                filtered_char_list(c.text)
                            )
                            if u_list:
                                char_dict["base"] = u_list
                        elif "type" in c.attrib:
                            t = c.attrib["type"]
                            if t in ["auxiliary", "punctuation"]:
                                if t == "auxiliary":
                                    t = "optional"
                                u_list = format_char_list(
                                    filtered_char_list(c.text)
                                )
                                if u_list:
                                    char_dict[t] = u_list
                    if char_dict:
                        if code in language_dict:
                            # print("Add information for", code)
                            if not code in language_chars:
                                # print("    Add entry for code to master dict:", code)
                                language_chars[code] = {}
                            if not script in language_chars[code]:
                                # print("    Add entry for script/code to master dict:", script)
                                language_chars[code][script] = {}

                            # Found best matching entry from language_dict
                            c_t_key = "%s_%s" % (code, territory)
                            c_s_key = "%s_%s" % (code, script)
                            all_key = "%s_%s_%s" % (code, script, territory)
                            found = False
                            for key in [all_key, c_t_key, c_s_key, code]:
                                if key in language_dict:
                                    found = True
                                    name = language_dict[key]
                                    try:
                                        del ignored_languages[key]
                                    except:
                                        pass
                                    break
                            if not found:
                                print(
                                    "Could not determine name for %s/%s/%s"
                                    % (script, code, territory)
                                )
                                name = "Unknown"

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

                            language_chars[code][script][territory] = {
                                "name": name,
                                "unicodes": char_dict,
                            }
                            # if territory in territory_dict:
                            #   language_chars[code][script][territory]["territory"] = territory_dict[territory]
                        else:
                            if code != "root":
                                print(f"Language is not in master list: {code}")
                    else:
                        pass
                        # print("    XML for %s (%s/%s/%s) contains no character information" % (language_dict[code], script, code, territory))

        print(f"Parsed {i} files.")

        for code in ignored_languages:
            del language_dict[code]
        clean_json_dir(sep_path)

        json_to_file(json_path, "languages", language_dict)
        json_to_file(json_path, "ignored", ignored_languages)
        for code, v in language_chars.items():
            # print("json_to_file:", "%s" % code)
            json_to_file(sep_path, "%s" % code, v)


if __name__ == "__main__":
    generate_language_data(zip_path)
