#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs, copy, json, os
import xml.etree.ElementTree as ET
from xmlhelpers import filtered_char_list


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


#def generate_language_data():
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
	file_not_found = []
	i = 0

	for code, name in language_dict.items():
		char_dict = {}
		lang_xml_path = os.path.join(xml_path, "%s.xml" % code)
		if not os.path.exists(lang_xml_path):
			#print "Not found:", lang_xml_path
			file_not_found.append(code)
		else:
			i += 1
			#print code, name
			root = ET.parse(lang_xml_path).getroot()
			ec = root.findall("characters/exemplarCharacters")
			for c in ec:
				if c.attrib == {}:
					# Main entry
					char_dict["main"] = filtered_char_list(c.text)
				elif "type" in c.attrib:
					t = c.attrib["type"]
					if t in ["auxiliary", "punctuation"]:
						char_dict[c.attrib["type"]] = filtered_char_list(c.text)
		if char_dict:
			language_chars[code] = {"name": name, "characters": char_dict}
			del ignored_languages[code]
		else:
			if code not in file_not_found:
				pass
				#print "XML file for %s (%s) contains no character information" % (name, code)
		#if i % 50 == 0:
		#	print i
	
	print "Parsed %i files." % i
	
	json_to_file(json_path, "language_characters", language_chars)
	json_to_file(json_path, "ignored", ignored_languages)
	sep_path = os.path.join(json_path, "languages")
	
	# Clean up the directory which contains the separate json files to avoid orphaned files
	for code in sorted(ignored_languages.keys()):
		try:
			#print "Remove", os.path.join(sep_path, "%s.json" % code)
			os.remove(os.path.join(sep_path, "%s.json" % code))
		except:
			pass
	
	for k, v in language_chars.items():
		json_to_file(sep_path, k, v)
	