#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from jsonhelpers import json_path, json_to_file, dict_from_file


languages_path = os.path.join(json_path, "languages")
overrides_path = os.path.join(json_path, "overrides")


def update_language_dict(language_dict, override_dict):
	
	for script, territory_dict in override_dict.items():
		print "Descending into script:", script
		if script in language_dict:
			print "Found script in original dict."
			# Check sub dicts
			d = language_dict[script]
			for territory, char_dict in territory_dict.items():
				print "   ", territory
				if territory in d:
					print "    Found territory in original dict."
					dd = language_dict[script][territory]
					print "    Compare:"
					print "**** Original:"
					for a, b in dd.items():
						print "    ", a, b
					print "**** Override:"
					for a, b in char_dict.items():
						print a, b
					for k, v in char_dict.items():
						print "       Look for", k
						if k in dd:
							print "            Found key in dict:", k
							if k == "name":
								print "            Override name:", v
								language_dict[script][territory]["name"] = v
								print language_dict
							if k == "unicodes":
								ddd = language_dict[script][territory][k]
								for cat, contents in v.items():
									ddd[cat] = contents
						else:
							print "    Add value for territory:", k, v
							language_dict[script][territory][k] = v
				else:
					print "    Add sub dict for territory:", territory, char_dict
					d[territory] = char_dict
		else:
			# Add complete sub dict
			print "Add sub dict for script:", script, territory_dict
			language_dict[script] = territory_dict
	return language_dict


if not(os.path.exists(os.path.join(json_path, "languages.json"))):
	print "JSON language data not found.\nPlease use the script 'generateJsonLangData.py' to generate it."
else:
	language_dict = dict_from_file(json_path, "languages")
	print "OK: Read %i language names." % len(language_dict)
	print [name for name in sorted(language_dict.keys())]
	
	master = {}
	
	for code in sorted(language_dict.keys()):
		file_name = "%s.json" % code
		if os.path.exists(os.path.join(languages_path, file_name)):
			language_dict = dict_from_file(languages_path, code)
			if os.path.exists(os.path.join(overrides_path, file_name)):
				print "INFO: Using override JSON file for '%s'" % code
				# TODO: Better updating of dicts to allow more granular overrides
				language_dict = update_language_dict(language_dict, dict_from_file(overrides_path, code))
		else:
			print "WARNING: Language '%s' requested, but JSON file not found." % code
			language_dict = {}
		#print language_dict
		if language_dict:
			for script, territory_dict in language_dict.items():
				for territory, char_dict in territory_dict.items():
					# Remove all but codepoint information
					for cat in ["base", "optional", "punctuation"]:
						char_list = char_dict["unicodes"].get(cat, [])
						char_list = [int(c.split()[0], 16) for c in char_list]
						if char_list:
							char_dict["unicodes"][cat] = char_list
			master[code] = language_dict
	
	json_to_file(json_path, "language_characters", master)