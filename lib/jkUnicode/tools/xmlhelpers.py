#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The dirty hacky stuff is outsourced into this file

from re import compile
from jkUnicode import getUnicodeChar

ur = compile("^u([0-9A-F]+)$") # Regex to match unicode sequences, e.g. \u0302


def split_all(l):
	a = l.split()
	r = []
	for b in a:
		r.extend(b.split("\\"))
	return r


def filtered_char_list(xml_char_list, debug=False):
	# Filter backslashes and other peculiarities of the XML format from the character list
	filtered1 = []
	filtered = []
	
	
	if xml_char_list[0] == "[" and xml_char_list[-1] == "]":
		xml_char_list = xml_char_list[1:-1]
	else:
		print "ERROR: Character list string from XML was not wrapped in []."
		return []
	
	if debug: print "Step 1: ****%s****" % xml_char_list
	
	xml_char_list = xml_char_list.replace("}{", "} {")
	
	if debug: print "Step 1a: ****%s****" % xml_char_list
	
	xml_char_list = xml_char_list.split()
	if debug: print "Step 2: %s" % xml_char_list
	
	for d in xml_char_list:
		if d[0] == "{" and len(d) > 1:
			d = d[1:]
		if d[-1] == "}" and len(d) > 1:
			d = d[:-1]
		e = split_all(d)
		if debug: print "e =", e
		filtered1.extend(e)
	
	# Remove duplicate entries
	filtered1 = list(set(filtered1))
	
	# Remove empty entries
	try:
		filtered1.remove("")
	except ValueError:
		pass
	
	for c in filtered1:
		m = ur.search(c)
		if m:
			c = getUnicodeChar(int(m.groups(0)[0], 16))
		else:
			if len(c) > 1:
				c = [d for d in c]
		filtered.extend(c)
	if debug: print filtered
	return sorted(list(set(filtered)))


if __name__ == "__main__":
	lists = [
		#r"[\u200C\u200D \u200F A {A\u0301} {E \u0302} {ij} \]]"
		u"[a á à â ǎ ā {a\\u1DC6}{a\\u1DC7} b ɓ c d e é è ê ě ē {e\\u1DC6}{e\\u1DC7} ɛ {ɛ\\u0301} {ɛ\\u0300} {ɛ\\u0302} {ɛ\\u030C} {ɛ\\u0304} {ɛ\\u1DC6}{ɛ\\u1DC7} f g h i í ì î ǐ ī {i\\u1DC6}{i\\u1DC7} j k l m n ń ǹ ŋ o ó ò ô ǒ ō {o\\u1DC6}{o\\u1DC7} ɔ {ɔ\\u0301} {ɔ\\u0300} {ɔ\\u0302} {ɔ\\u030C} {ɔ\\u0304} {ɔ\\u1DC6}{ɔ\\u1DC7} p r s t u ú ù û ǔ ū {u\\u1DC6}{u\\u1DC7} v w y z]"
	]

	for cl in lists:
		ll = filtered_char_list(cl, True)
		print "Result:", ll