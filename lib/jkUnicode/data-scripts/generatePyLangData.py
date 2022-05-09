#!/usr/bin/env python

import os
from jkUnicode.tools.jsonhelpers import json_path, json_to_file, dict_from_file

print(f"JSON path: {json_path}")
languages_path = os.path.join(json_path, "languages")
overrides_path = os.path.join(json_path, "overrides")


def update_language_dict(language_dict, override_dict):

    for script, territory_dict in override_dict.items():
        if script in language_dict:
            # Check sub dicts
            for territory, char_dict in territory_dict.items():
                if territory in language_dict[script]:
                    for k, v in char_dict.items():
                        if k in language_dict[script][territory]:
                            if k == "name":
                                language_dict[script][territory]["name"] = v
                            elif k == "unicodes":
                                for cat, contents in v.items():
                                    language_dict[script][territory][
                                        "unicodes"
                                    ][cat] = contents
                            else:
                                print(
                                    "WARNING: Unknown key in territory "
                                    f"ignored: {k}"
                                )
                        else:
                            language_dict[script][territory][k] = v
                else:
                    language_dict[script][territory] = char_dict
        else:
            # Add complete sub dict
            language_dict[script] = territory_dict
    # return language_dict # dict is changed in place


if not (os.path.exists(os.path.join(json_path, "languages.json"))):
    print(
        "JSON language data not found.\n"
        "Please use the script 'generateJsonLangData.py' to generate it."
    )
else:
    language_names = dict_from_file(json_path, "languages")
    print("OK: Read %i language names." % len(language_names))
    # print([name for name in sorted(language_names.keys())])

    if os.path.exists(os.path.join(json_path, "languages_additional.json")):
        # Read additional languages which are only added via override file
        try:
            add_language_names = dict_from_file(
                json_path, "languages_additional"
            )
            print(
                "OK: Read %i additional language names."
                % len(add_language_names)
            )
            for key, value in add_language_names.items():
                language_names[key] = value
        except ValueError:
            # Probably an empty file
            print(
                "WARNING: Could not read JSON data from "
                "'languages_additional.json', skipped."
            )

    ignored = {}
    if os.path.exists(os.path.join(json_path, "ignored.json")):
        # Keep track of ignored languages, they may have been added via
        # languages_additional.json
        try:
            ignored = dict_from_file(json_path, "ignored")
        except ValueError:
            # Probably an empty file
            print(
                "WARNING: Could not read JSON data from 'ignored.json', "
                "skipped."
            )

    master = {}

    for code in sorted(language_names.keys()):
        file_name = "%s.json" % code
        if os.path.exists(os.path.join(languages_path, file_name)):
            language_dict = dict_from_file(languages_path, code)
            if os.path.exists(os.path.join(overrides_path, file_name)):
                print("INFO: Using override JSON file for '%s'" % code)
                update_language_dict(
                    language_dict, dict_from_file(overrides_path, code)
                )
        else:
            language_dict = {}
            if os.path.exists(os.path.join(overrides_path, file_name)):
                print(
                    "INFO: Using override JSON file for custom definition "
                    f"'{code}'"
                )
                language_dict = dict_from_file(overrides_path, code)
            elif not "_" in code or not code.split("_")[0] in language_names:
                # The language code is territory or script specific, but the
                # parent language file is not found.
                print(
                    f"WARNING: Language '{code}' requested, but JSON file "
                    "not found."
                )

        if language_dict:
            for script, territory_dict in language_dict.items():
                for territory, char_dict in territory_dict.items():
                    # Remove all but codepoint information from the "unicodes"
                    # dict key
                    for cat in ["base", "optional", "punctuation"]:
                        char_list = char_dict["unicodes"].get(cat, [])
                        # Store the chars as int codes instead of hex string
                        char_list = [int(c.split()[0], 16) for c in char_list]
                        if char_list:
                            char_dict["unicodes"][cat] = char_list
            master[code] = language_dict

    json_to_file(json_path, "language_characters", master)
    json_to_file(json_path, "languages", language_names)
    json_to_file(json_path, "ignored", ignored)
