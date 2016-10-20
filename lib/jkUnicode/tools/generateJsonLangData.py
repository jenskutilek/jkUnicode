#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy, os
import xml.etree.ElementTree as ET
from xmlhelpers import filtered_char_list
from jkUnicode.aglfn import getGlyphnameForUnicode
from jsonhelpers import json_path, json_to_file


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


def format_char_list(char_list):
	return [u"0x%04X %s %s" % (ord(cc), cc, getGlyphnameForUnicode(ord(cc))) for cc in char_list]


#def generate_language_data():
if not(os.path.exists(en_path)):
	print "XML language data not found.\nPlease use the shell script 'updateLangData.sh' to download it."
else:
	# Extract language names from the English data file

	root = ET.parse(en_path).getroot()

	language_dict = extract_dict(root, "localeDisplayNames/languages/language")
	try:
		# Root is not a language, but the template file
		del language_dict["root"]
	except:
		pass
	print "OK: Read %i language names." % len(language_dict)

	script_dict = extract_dict(root, "localeDisplayNames/scripts/script")
	print "OK: Read %i script names." % len(script_dict)

	json_to_file(json_path, "scripts", script_dict)

	print "Parsing language character data ..."

	language_chars = {}
	ignored_languages = copy.deepcopy(language_dict)
	
	sep_path = os.path.join(json_path, "languages")
	
	# Clean up the directory which contains the separate json files to avoid orphaned files
	for name in os.listdir(sep_path):
		if not name[0] == "." and name.lower().endswith(".json"):
			try:
				#print "Remove", os.path.join(sep_path, name)
				os.remove(os.path.join(sep_path, name))
			except:
				print "WARNING: Could not remove file before regenerating it:", os.path.join(sep_path, name)
	
	i = 0

	for filename in os.listdir(xml_path):
		if not filename[0] == "." and filename.lower().endswith(".xml"):
			char_dict = {}
			lang_xml_path = os.path.join(xml_path, filename)
			i += 1
			#print code, name
			root = ET.parse(lang_xml_path).getroot()
			
			# Extract code
			code = root.findall("identity/language")
			if len(code) == 0:
				print "ERROR: Language code not found in file '%s'" % lang_xml_path
				code = None
			elif len(code) == 1:
				code = code[0].attrib["type"]
			else:
				print "ERROR: Language code ambiguous in file '%s'" % lang_xml_path
				code = None
			
			# Extract script
			script = root.findall("identity/script")
			if len(script) == 0:
				#print "WARNING: Script not found in file '%s'" % lang_xml_path
				script = "DFLT"
			elif len(script) == 1:
				script = script[0].attrib["type"]
			else:
				print "ERROR: Script ambiguous in file '%s'" % lang_xml_path
				script = None
			
			# Extract territory
			territory = root.findall("identity/territory")
			if len(territory) == 0:
				#print "WARNING: Territory not found in file '%s'" % lang_xml_path
				territory = "dflt"
			elif len(territory) == 1:
				territory = territory[0].attrib["type"]
			else:
				print "ERROR: Territory ambiguous in file '%s'" % lang_xml_path
				territory = None
			
			# Extract characters
			ec = root.findall("characters/exemplarCharacters")
			for c in ec:
				if c.attrib == {}:
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
			if char_dict:
				if code in language_dict:
					print "Add information for", code
					if not code in language_chars:
						language_chars[code] = {"name": language_dict[code], "variants": {}}
					language_chars[code]["variants"]["%s %s" % (script, territory)] = char_dict
				else:
					print "Language is not in master list:", code
				try:
					del ignored_languages[code]
				except:
					pass
				#print language_chars[code]
			else:
				print "    XML for %s (%s-%s-%s) contains no character information" % (language_dict[code], script, code, territory)
			#if i % 50 == 0:
			#	print i
	
	print "Parsed %i files." % i
	
	#json_to_file(json_path, "language_characters", language_chars)
	#for code in ignored_languages:
	#	if not "_" in code:
	#		del language_dict[code]
	
	#for code in ignored_languages:
	#	if "_" in code and not code.split("_", 1)[0] in language_dict:
	#		del language_dict[code]
	
	json_to_file(json_path, "languages", language_dict)
	json_to_file(json_path, "ignored", ignored_languages)
	for k, v in language_chars.items():
		print "json_to_file:", "%s" % k
		json_to_file(sep_path, "%s" % k, v)
	