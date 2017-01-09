#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os, weakref
from jkUnicode import UniInfo
from jkUnicode.tools.jsonhelpers import json_path, json_to_file, dict_from_file


# These unicode points are ignored when scanning for orthography support
IGNORED_UNICODES = [
	# Minute and second appear in lots of language definitions in CLDR, but are not in very many fonts.
	0x2032, # minute
	0x2033, # second
]


ui = UniInfo(0)

def cased(codepoint_list):
	result = []
	for c in codepoint_list:
		ui.unicode = c
		if ui.lc_mapping:
			result.append(ui.lc_mapping)
		elif ui.uc_mapping:
			result.append(ui.uc_mapping)
	return list(set(result))



class Orthography(object):
	
	def __init__(self, info_obj, code, script, territory, info_dict):
		self._info = weakref.ref(info_obj)
		self.code = code
		self.script = script
		self.territory = territory
		self.from_dict(info_dict)
	
	
	def from_dict(self, info_dict):
		self.name = info_dict.get("name", None)
		uni_info = info_dict.get("unicodes", {})
		
		# Add the unicode points, and also the cased variants of the unicode points of each category.
		u_list = uni_info.get("base", [])
		self.unicodes_base        = set(u_list + cased(u_list)) - self.info.ignored_unicodes
		
		u_list = uni_info.get("optional", [])
		self.unicodes_optional    = set(u_list + cased(u_list)) - self.unicodes_base - self.info.ignored_unicodes
		
		u_list = uni_info.get("punctuation", [])
		self.unicodes_punctuation = set(u_list + cased(u_list)) - self.info.ignored_unicodes
		
		# Additional sets to speed up later calculations
		self.unicodes_base_punctuation = self.unicodes_base | self.unicodes_punctuation
		self.unicodes_any = self.unicodes_base | self.unicodes_optional | self.unicodes_punctuation
		
		self.scan_ok = False
	
	
	def fill_from_default_orthography(self):
		# Sometimes the base unicodes are empty for a variant.
		# Try to fill them in from the default variant.
		# Call this only after the whole list of orthographies is present, or it will fail.
		if self.territory != "dflt":
			#print self.code, self.script, self.territory
			parent = self.info.orthography(self.code, self.script)
			if parent is None:
				print "WARNING: No parent orthography found for %s/%s/%s" % (self.code, self.script, self.territory)
			else:
				#print "    Parent:", parent.code, parent.script, parent.territory
				# Set attributes from parent (there may be empty attributes remaining ...?)
				for attr in ["unicodes_base", "unicodes_optional", "unicodes_punctuation"]:
					if getattr(self, attr) == set():
						parent_set = getattr(parent, attr)
						if parent_set:
							#print "    Filled from parent:", attr
							setattr(self, attr, parent_set)
	
	
	def support_full(self):
		if self.num_missing_base == 0 and self.num_missing_optional == 0 and self.num_missing_punctuation == 0:
			return True
		return False
	
	
	def support_basic(self):
		if self.num_missing_base == 0 and self.num_missing_punctuation == 0:
			return True
		return False
	
	
	def support_minimal(self):
		if self.num_missing_base == 0 and self.num_missing_optional != 0 and self.num_missing_punctuation != 0:
			return True
		return False
	
	
	def almost_supported_full(self, max_missing = 5):
		if 0 < self.num_missing_all <= max_missing:
			return True
		return False
	
	
	def almost_supported_basic(self, max_missing = 5):
		if 0 < self.num_missing_base <= max_missing:
			return True
		return False
	
	
	def almost_supported_punctuation(self, max_missing = 5):
		if self.num_missing_base == 0 and 0 < self.num_missing_punctuation <= max_missing:
			return True
		return False
	
	
	def uses_unicode_base(self, u):
		# Is the unicode used by this orthography in the base set?
		# This is relatively slow. Use OrthographyInfo.build_reverse_cmap if you need to access it more often.
		if u in self.unicodes_base_punctuation:
			return True
		return False
	
	
	def uses_unicode_any(self, u):
		# Is the unicode used by this orthography in any set?
		# This is relatively slow. Use OrthographyInfo.build_reverse_cmap if you need to access it more often.
		if u in self.unicodes_any:
			return True
		return False
	
	
	def scan_cmap(self):
		cmap_set = set(self.info.cmap)
		# Check for missing chars
		self.missing_base        = self.unicodes_base        - cmap_set
		self.missing_optional    = self.unicodes_optional    - cmap_set
		self.missing_punctuation = self.unicodes_punctuation - cmap_set
		self.missing_all = self.missing_base | self.missing_optional | self.missing_punctuation
		
		self.num_missing_base        = len(self.missing_base)
		self.num_missing_optional    = len(self.missing_optional)
		self.num_missing_punctuation = len(self.missing_punctuation)
		self.num_missing_all = len(self.missing_all)
		
		# Calculate percentage
		self.base_pc        = 1 - self.num_missing_base / len(self.unicodes_base) if self.unicodes_base else 0
		self.optional_pc    = 1 - self.num_missing_optional / len(self.unicodes_optional) if self.unicodes_optional else 0
		self.punctuation_pc = 1 - self.num_missing_punctuation / len(self.unicodes_punctuation) if self.unicodes_punctuation else 0
		
		self.scan_ok = True
	
	
	def forget_cmap(self):
		self.scan_ok = False
	
	
	@property
	def info(self):
		# self._info is a weakref, call it to return its object
		return self._info()
	
	
	@property
	def name(self):
		return self._name
	
	
	@name.setter
	def name(self, value):
		self._name = value
	
	
	def __cmp__(self, other):
		# For sorting
		if self.name > other.name:
			return 1
		elif self.name == other.name:
			return 0
		else:
			return -1
	
	
	def __eq__(self, other):
		if self.name == other.name:
			return True
		return False
	
	
	def __ne__(self, other):
		if self.name == other.name:
			return False
		return True
	
	
	def __repr__(self):
		return u'<Orthography "%s">' % self.name.encode("ascii", errors="ignore")



class OrthographyInfo(object):
	def __init__(self):
		data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "json")
		master = dict_from_file(data_path, "language_characters")
		
		self.ignored_unicodes = set(IGNORED_UNICODES)
		self.orthographies = []
		self._index = {}
		i = 0
		for code, script_dict in master.items():
			#print code, script_dict
			for script, territory_dict in script_dict.items():
				#print script, territory_dict
				for territory, info in territory_dict.items():
					#print territory, info
					self.orthographies.append(Orthography(self, code, script, territory, info))
					self._index[(code, script, territory)] = i
					i += 1
		for o in self.orthographies:
			o.fill_from_default_orthography()
		
		self._language_names  = dict_from_file(data_path, "languages")
		self._script_names    = dict_from_file(data_path, "scripts")
		self._territory_names = dict_from_file(data_path, "territories")
		
		self._cmap = None
		self._reverse_cmap = None
	
	
	@property
	def cmap(self):
		if self._cmap is None:
			return {}
		return self._cmap
	
	
	@cmap.setter
	def cmap(self, value=None):
		if value is None:
			self._cmap = None
			for o in self.orthographies:
				o.forget_cmap()
		else:
			self._cmap = value
			for o in self.orthographies:
				o.scan_cmap()
	
	
	def build_reverse_cmap(self):
		# Build a map from a unicode to all orthographies (index) using it.
		self._reverse_cmap = {}
		for i, o in enumerate(self.orthographies):
			for u in o.unicodes_base_punctuation:
				if u in self._reverse_cmap:
					self._reverse_cmap[u].append(i)
				else:
					self._reverse_cmap[u] = [i]
	
	
	def orthography(self, code, script="DFLT", territory="dflt"):
		# Access an orthography by its language, script and territory code.
		i = self._index.get((code, script, territory), None)
		if i is None:
			return None
		return self.orthographies[i]
	
	
	def get_orthographies_for_char(self, char):
		# Get a list of orthographies which use a supplied character at base level.
		if not self._reverse_cmap:
			self.build_reverse_cmap()
		ol = self._reverse_cmap.get(ord(char), [])
		return [self.orthographies[i] for i in ol]
	
	
	def get_orthographies_for_unicode(self, u):
		# Get a list of orthographies which use a supplied codepoint at base level.
		if not self._reverse_cmap:
			self.build_reverse_cmap()
		ol = self._reverse_cmap.get(u, [])
		return [self.orthographies[i] for i in ol]
	
	
	def get_orthographies_for_unicode_any(self, u):
		# Get a list of orthographies which use a supplied codepoint at any level.
		#ol = self._reverse_cmap.get(u, [])
		return [o for o in self.orthographies if o.uses_unicode_any(u)]
	
	
	# Nice names for language, script, territory
	
	def get_language_name(self, code):
		# Return the nice name for a language by code
		return self._language_names.get(code, code)
	
	
	def get_script_name(self, code):
		# Return the nice name for a script by code
		if code == "DFLT":
			return "Default"
		else:
			return self._script_names.get(code, code)
	
	
	def get_territory_name(self, code):
		# Return the nice name for a territory by code
		if code == "dflt":
			return "Default"
		else:
			return self._territory_names.get(code, code)
	
	
	# Convenience functions
	
	def get_supported_orthographies(self, full_only=False):
		# Get a list of supported orthographies for a character list.
		# full_only: Return only orthographies which have also all optional characters present.
		if full_only:
			return [o for o in self.orthographies if o.support_full()]
		return [o for o in self.orthographies if o.support_basic()]
	
	
	def get_supported_orthographies_minimum(self):
		# Get a list of minimally supported orthographies for a character list.
		return [o for o in self.orthographies if o.support_minimal()]
	
	
	def get_almost_supported(self, max_missing=5):
		return [o for o in self.orthographies if o.almost_supported_basic(max_missing)]
	
	
	def get_almost_supported_punctuation(self):
		return [o for o in self.orthographies if o.almost_supported_punctuation()]
	
	
	#def __getitem__(self, key):
	#	return self.orthographies[key]
	
	
	def __len__(self):
		return len(self.orthographies)
	
	
	def __repr__(self):
		return u"<OrthographyInfo with %i orthographies>" % len(self)
	
	
	# Very convenient convenience functions
	
	def print_report(self, otlist, attr):
		otlist.sort()
		for ot in otlist:
			print "\n%s" % ot.name
			for u in sorted(list(getattr(ot, attr))):
				ui.unicode = u
				print "    0x%04X\t%s\t%s" % (u, ui.glyphname, ui.name.title())

	def report_supported(self, full_only=False):
		m = self.get_supported_orthographies(full_only)
		print "The font supports %i orthographies:" % len(m)
		m.sort()
		for ot in m: print ot.name
	
	
	def report_missing_punctuation(self):
		m = self.get_almost_supported_punctuation()
		print "Orthographies which can be supported by adding punctuation characters:"
		self.print_report(m, "missing_punctuation")
	
	
	def report_near_misses(self, n):
		m = self.get_almost_supported(n)
		print "Orthographies which can be supported with max. %i additional %s:" % (n, "character" if n == 1 else "characters")
		self.print_report(m, "missing_base")



# Test functions

def test_scan():
	from time import time
	from fontTools.ttLib import TTFont
	from htmlGenerator.fonttools.sfnt import get_cmap
	from jkUnicode import get_expanded_glyph_list
	
	font_path = "/Users/jens/Documents/Schriften/Hertz/Hertz-Book.ttf"
	
	print "Scanning font for orthographic support:"
	print font_path
	
	# Get a character map from a font to scan.
	cmap = get_cmap(TTFont(font_path))
	start = time()
	o = OrthographyInfo()
	print o
	
	
	# List known orthographies
	for ot in sorted(o.orthographies):
		print ot.name, ot.code
	
	o.cmap = cmap
	
	# Scan for full, base and minimal support of the font's cmap
	full = o.get_supported_orthographies(full_only=True)
	base = o.get_supported_orthographies(full_only=False)
	mini = o.get_supported_orthographies_minimum()
	stop = time()
	
	print "\nFull support:", len(full), "orthography" if len(base) == 1 else "orthographies"
	print ", ".join([x.name for x in full])
	
	base = [r for r in base if not r in full]
	print "\nBasic support:", len(base), "orthography" if len(base) == 1 else "orthographies"
	print ", ".join([x.name for x in base])
	
	mini = [r for r in mini if not r in full]
	print "\nMinimal support (no punctuation):", len(mini), "orthography" if len(mini) == 1 else "orthographies"
	print ", ".join([x.name for x in mini])
	
	# Timing information
	print stop - start
	
	
	# Output info about one orthography
	ot = o.orthography("en", "DFLT", "ZA")
	print "\nOrthography:", ot.name
	print list(ot.unicodes_base)
	
	
	# Scan the font again, but allow for a number of missing characters
	print
	n = 3
	o.report_near_misses(n)
	

def test_reverse():
	from time import time
	
	print "\nTest of the Reverse CMAP functions"
	
	c = u"ö"
	o = OrthographyInfo()
	
	print "\nBuild reverse CMAP:", 
	start = time()
	o.build_reverse_cmap()
	stop = time()
	d = (stop - start) * 1000
	print "%0.2f ms" % d
	
	u = ord(c)
	
	start = time()
	result1 = o.get_orthographies_for_unicode(u)
	stop = time()
	d = (stop - start) * 1000
	print "Use cached lookup:  %0.2f ms" % d
	
	start = time()
	result2 = o.get_orthographies_for_unicode_any(u)
	stop = time()
	d = (stop - start) * 1000
	print "Use uncached lookup: %0.2f ms" % d
	
	
	print u"'%s' is used in:" % c
	for ot in sorted(result1):
		print "   ", ot.name



if __name__ == "__main__":
	test_scan()
	test_reverse()