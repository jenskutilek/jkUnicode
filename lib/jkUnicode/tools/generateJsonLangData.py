#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy, os
import xml.etree.ElementTree as ET
from xmlhelpers import filtered_char_list
from jkUnicode.aglfn import getGlyphnameForUnicode
from jsonhelpers import json_path, json_to_file, clean_json_dir


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
	
	i = 0

	for filename in os.listdir(xml_path):
		if not filename[0] == "." and filename.lower().endswith(".xml"): # and filename.startswith("zh"):
			char_dict = {}
			lang_xml_path = os.path.join(xml_path, filename)
			i += 1
			root = ET.parse(lang_xml_path).getroot()
			#print "\nFile:", lang_xml_path
			
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
			#print "    Code:", code
			
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
			#print "    Script:", script
			
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
			#print "    Territory:", territory
			
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
					#print "Add information for", code
					if not code in language_chars:
						#print "    Add entry for code to master dict:", code
						language_chars[code] = {}
					if not script in language_chars[code]:
						#print "    Add entry for script/code to master dict:", script
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
							try: del ignored_languages[key]
							except: pass
							break
					if not found:
						print "Could not determine name for %s/%s/%s" % (script, code, territory)
						name = "Unknown"
					if script != "DFLT":
						name += " (%s)" % script_dict[script] if script in script_dict else script
					
					language_chars[code][script][territory] = {"name": name, "unicodes": char_dict}
				else:
					print "Language is not in master list:", code
			else:
				pass
				#print "    XML for %s (%s/%s/%s) contains no character information" % (language_dict[code], script, code, territory)
	
	print "Parsed %i files." % i
	
	for code in ignored_languages:
		del language_dict[code]
	clean_json_dir(sep_path)
	
	json_to_file(json_path, "languages", language_dict)
	json_to_file(json_path, "ignored", ignored_languages)
	for code, v in language_chars.items():
		#print "json_to_file:", "%s" % code
		json_to_file(sep_path, "%s" % code, v)
	