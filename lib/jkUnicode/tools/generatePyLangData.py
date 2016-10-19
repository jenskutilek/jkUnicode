#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from jsonhelpers import json_path, json_to_file, dict_from_file


languages_path = os.path.join(json_path, "languages")
overrides_path = os.path.join(json_path, "overrides")


if not(os.path.exists(os.path.join(json_path, "languages.json"))):
	print "JSON language data not found.\nPlease use the script 'generateJsonLangData.py' to generate it."
else:
	language_dict = dict_from_file(json_path, "languages")
	print "OK: Read %i language names." % len(language_dict)
	print language_dict
	
	language_characters = {}
	
	for code in sorted(language_dict.keys()):
		file_name = "%s.json" % code
		if os.path.exists(os.path.join(overrides_path, file_name)):
			print "INFO: Using override JSON file for '%s'" % code
			language_char_dict = dict_from_file(overrides_path, code)
		elif os.path.exists(os.path.join(languages_path, file_name)):
			language_char_dict = dict_from_file(languages_path, code)
		else:
			print "WARNING: Language '%s' requested, but JSON file not found." % code
			language_char_dict = {}
		#print language_char_dict
		if language_char_dict:
			language_characters[code] = language_char_dict
	
	json_to_file(json_path, "language_characters", language_characters)