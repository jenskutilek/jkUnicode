#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from os.path import exists
from string import strip

aglfnFooter = '''
	# custom additions
	'NULL': 0x0000,
	'CR': 0xd,
	'twosuperior': 0x00B2,
	'threesuperior': 0x00B3,
	'onesuperior': 0x00B9,
	'fi': 0xfb01,
	'fl': 0xfb02,
	}

unicodeToName = {value: key for key, value in nameToUnicode.iteritems()}

unicodeToName = {value: key for key, value in nameToUnicode.iteritems()}

def getUnicodeForGlyphname(name):
	"""Return the Unicode value as integer or None that is assigned to the specified glyph name. It handles AGLFN names, uniXXXX names, uXXXXX names, ligature names, variant names, and PUA-encoded ornament names (orn001 - orn999, starting at 0xEA01).

	:param name: The glyph name.
	:type name: str"""
	ornName = compile("^orn[0-9]{3}$")
	if "_" in name:
		return None
	elif "." in name[1:]:
		return None
	elif name in nameToUnicode.keys():
		return nameToUnicode[name]
	elif name[0:3] == "uni" and len(name) == 7:
		return int(name[3:], 16)
	elif name[0] == "u" and len(name) == 6:
		try:
			return int(name[1:], 16)
		except:
			return None
	elif ornName.match(name):
		return 0xea00 + int(name[3:6])
	else:
		return None

def getGlyphnameForUnicode(code):
	"""Return the name as string or None that is assigned to the specified Unicode value.

	:param code: The codepoint.
	:type code: int"""
	if code is None:
		return None
	elif code in unicodeToName.keys():
		return unicodeToName[code]
	elif code < 0xffff:
		return "uni%04X" % code
	else:
		return "u%05X" % code

'''

# Unicode names
print "Unicode Character Names ..."
if exists("UnicodeData.txt"):
	with codecs.open("../uniName.py", 'w', encoding='utf-8') as outfile:
		outfile.write("# This is a generated file, use tools/generatePyUniData.py to edit and regenerate.\n\nuniName = {")
		with codecs.open("UnicodeData.txt", encoding='utf-8') as f:
			for line in f:
				elements = line.split(';')
				outfile.write("\n\t0x%s: '%s'," % (elements[0], elements[1]))
				#print elements
		outfile.write("\n}")
	print "OK."
else:
	print "    WARNING: File UnicodeData.txt not found, Unicode name data not regenerated."

# Unicode names
print "Unicode Case Mappings ..."
if exists("UnicodeData.txt"):
	with codecs.open("../uniCase.py", 'w', encoding='utf-8') as outfile:
		outfile.write("# This is a generated file, use tools/generatePyUniData.py to edit and regenerate.\n\nuniUpperCaseMapping = {")
		uc = []
		lc = []
		with codecs.open("UnicodeData.txt", encoding='utf-8') as f:
			for line in f:
				elements = line.strip().split(';')
				
				# Uppercase mapping
				ucm = elements[14]
				if ucm:
					uc.append((elements[0], ucm))
				
				# Lowercase mapping
				lcm = elements[13]
				if lcm:
					lc.append((elements[0], lcm))
				#print elements
		for item in uc:
			outfile.write("\n\t0x%s: 0x%s," % item)
		outfile.write("\n}\n\nuniLowerCaseMapping = {")
		for item in lc:
			outfile.write("\n\t0x%s: 0x%s," % item)
		outfile.write("\n}\n")
	print "OK."
else:
	print "WARNING: File UnicodeData.txt not found, Unicode name data not regenerated."

# Unicode category names
print "Unicode Categories ..."
if exists("UnicodeData.txt"):
	with codecs.open("../uniCat.py", 'w', encoding='utf-8') as outfile:
		outfile.write("# This is a generated file, use tools/generatePyUniData.py to edit and regenerate.\n\nuniCat = {")
		with codecs.open("UnicodeData.txt", encoding='utf-8') as f:
			for line in f:
				elements = line.split(';')
				outfile.write("\n\t0x%s: '%s'," % (elements[0], elements[2]))
				#print elements
		outfile.write("\n}")
	print "OK."
else:
	print "WARNING: File UnicodeData.txt not found, Unicode category data not regenerated."

# Unicode decomposition
print "Unicode Decomposition Mappings ..."
if exists("UnicodeData.txt"):
	with codecs.open("../uniDecomposition.py", 'w', encoding='utf-8') as outfile:
		outfile.write("# This is a generated file, use tools/generatePyUniData.py to edit and regenerate.\n\nuniDecompositionMapping = {")
		dc = []
		with codecs.open("UnicodeData.txt", encoding='utf-8') as f:
			for line in f:
				elements = line.strip().split(';')
				
				# Decomposition mapping
				dcm = elements[5]
				#print elements[0], dcm
				if dcm:
					codes = dcm.split(" ")
					if not codes[0].startswith("<"):
						dc.append((elements[0], codes))
				
		for code, decomp_sequence in dc:
			outfile.write("\n\t0x%s: [%s]," % (code, ", ".join(["0x%s" % d for d in decomp_sequence])))
		outfile.write("\n}\n")
	print "OK."
else:
	print "WARNING: File UnicodeData.txt not found, Unicode name data not regenerated."

# Adobe Glyph List for New Fonts
print "AGLFN ..."
if exists("aglfn.txt"):
	with codecs.open("../aglfn.py", 'w', encoding='utf-8') as outfile:
		outfile.write("# -*- coding: utf-8 -*-\n# This is a generated file, use tools/generatePyUniData.py to edit and regenerate.\n\nfrom re import match, compile\n\nnameToUnicode = {")
		with codecs.open("aglfn.txt", encoding='utf-8') as f:
			for line in f:
				if line[0] != "#":
					elements = line.split(';')
					outfile.write("\n\t'%s': 0x%s, # %s" % (elements[1], elements[0], strip(elements[2])))
				#print elements
		outfile.write(aglfnFooter)
	print "OK."
else:
	print "WARNING: File aglfn.txt not found, AGLFN data not regenerated."
