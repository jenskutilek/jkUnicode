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
	c = xml_char_list
	
	filtered1 = []
	filtered = []
	
	
	if xml_char_list[0] == "[" and xml_char_list[-1] == "]":
		xml_char_list = xml_char_list[1:-1]
	if debug: print "Step 1: ****%s****" % xml_char_list
	
	xml_char_list = xml_char_list.split()
	if debug: print "Step 2: %s" % xml_char_list
	
	for d in xml_char_list:
		if d[0] == "{":
			d = d[1:]
		if d[-1] == "}":
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
	return sorted(filtered)


if __name__ == "__main__":
	lists = [
		r"[\u200C\u200D \u200F A {A\u0301} {E \u0302} {ij} \]]"
	]

	for cl in lists:
		ll = filtered_char_list(cl, True)
		print "Result:", ll