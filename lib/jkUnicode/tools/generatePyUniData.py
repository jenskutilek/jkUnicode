#!/usr/bin/env python

import codecs
from os.path import exists
from string import strip

aglfnFooter = """
	# special FSI
	'NULL': 0x0000,
	'CR': 0xd,
	'twosuperior': 0x00B2,
	'threesuperior': 0x00B3,
	'onesuperior': 0x00B9,
	'Gcommaaccent': 0x122,
	'gcommaaccent': 0x123,
	'Kcommaaccent': 0x136,
	'kcommaaccent': 0x137,
	'Lcommaaccent': 0x13b,
	'lcommaaccent': 0x13c,
	'Ncommaaccent': 0x145,
	'ncommaaccent': 0x146,
	'Rcommaaccent': 0x156,
	'rcommaaccent': 0x157,
	'Scommaaccent': 0x218,
	'scommaaccent': 0x219,
	'Tcommaaccent': 0x162,
	'tcommaaccent': 0x163,
	'afii61352': 0x2116,
	'fi': 0xfb01,
	'fl': 0xfb02,
	}

def getUnicodeForGlyphname(name):
	ornName = compile("^orn[0-9]{3}$")
	if "_" in name:
		return None
	elif name in nameToUnicode.keys():
		return nameToUnicode[name]
	elif name[0:3] == "uni" and len(name) == 7:
		return int(name[3:], 16)
	elif name[0] == "u" and len(name) == 6:
		return int(name[1:], 16)
	elif ornName.match(name):
		return 0xea00 + int(name[3:6])
	else:
		return None
"""

# Unicode names
if exists("UnicodeData.txt"):
	with codecs.open("../uniName.py", 'w', encoding='utf-8') as outfile:
		outfile.write("# This is a generated file, use tools/generatePyUniData.py to edit and regenerate.\n\nuniName = {")
		with codecs.open("UnicodeData.txt", encoding='utf-8') as f:
			for line in f:
				elements = line.split(';')
				outfile.write("\n\t0x%s: '%s'," % (elements[0], elements[1]))
				#print elements
		outfile.write("\n}")
else:
	print "WARNING: File UnicodeData.txt not found, Unicode name data not regenerated."

# Unicode category names
if exists("UnicodeData.txt"):
	with codecs.open("../uniCat.py", 'w', encoding='utf-8') as outfile:
		outfile.write("# This is a generated file, use tools/generatePyUniData.py to edit and regenerate.\n\nuniCat = {")
		with codecs.open("UnicodeData.txt", encoding='utf-8') as f:
			for line in f:
				elements = line.split(';')
				outfile.write("\n\t0x%s: '%s'," % (elements[0], elements[2]))
				#print elements
		outfile.write("\n}")
else:
	print "WARNING: File UnicodeData.txt not found, Unicode category data not regenerated."

# Adobe Glyph List for New Fonts
if exists("aglfn.txt"):
	with codecs.open("../aglfn.py", 'w', encoding='utf-8') as outfile:
		outfile.write("# This is a generated file, use tools/generatePyUniData.py to edit and regenerate.\n\nfrom re import match, compile\n\nnameToUnicode = {")
		with codecs.open("aglfn.txt", encoding='utf-8') as f:
			for line in f:
				if line[0] != "#":
					elements = line.split(';')
					outfile.write("\n\t'%s': 0x%s, # %s" % (elements[1], elements[0], strip(elements[2])))
				#print elements
		outfile.write(aglfnFooter)
else:
	print "WARNING: File aglfn.txt not found, AGLFN data not regenerated."
