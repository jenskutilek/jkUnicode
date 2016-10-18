#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs, copy, json, os
import xml.etree.ElementTree as ET

xml_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "core", "common", "main")
en_path  = os.path.join(xml_path, "en.xml")


def extract_dict(root, key):
	elements = root.findall(key)
	d = {e.attrib["type"]: e.text for e in elements}
	return d


def extract_char_dict(root, key):
	elements = root.findall(key)
	d = {e.attrib["type"]: e.text for e in elements}
	return d


def json_to_file(path, file_name, obj):
	with codecs.open(os.path.join(path, "%s.json" % file_name), "w", "utf-8") as f:
		json.dump(obj, f, ensure_ascii=False, indent=4, sort_keys=True)


if not(os.path.exists(en_path)):
	print "XML language data not found.\nPlease use the shell script 'updateLangData.sh' to download it."
else:
	# Extract language names from the English data file

	root = ET.parse(en_path).getroot()
	
	language_dict = extract_dict(root, "localeDisplayNames/languages/language")
	print "OK: Read %i language names." % len(language_dict)

	script_dict = extract_dict(root, "localeDisplayNames/scripts/script")
	print "OK: Read %i script names." % len(script_dict)
	
	json_path = os.path.join(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0], "json")
	
	json_to_file(json_path, "languages", language_dict)
	json_to_file(json_path, "scripts", script_dict)
	
	print "Parsing language character data ..."
	
	language_chars = {}
	ignored_languages = copy.deepcopy(language_dict)
	
	for code in language_dict.keys():
		char_dict = {}
		lang_xml_path = os.path.join(xml_path, "%s.xml" % code)
		if os.path.exists(lang_xml_path):
			root = ET.parse(en_path).getroot()
			ec = root.findall("characters/exemplarCharacters")
			for c in ec:
				if c.attrib == {}:
					# Main entry
					char_dict["main"] = c.text.strip("[]").split()
				elif "type" in c.attrib:
					char_dict[c.attrib["type"]] = c.text.strip("[]").split()
		if char_dict:
			language_chars[code] = char_dict
		else:
			del ignored_languages[code]
	
	json_to_file(json_path, "language_characters", language_chars)
	json_to_file(json_path, "ignored", ignored_languages)