#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os, weakref
from jkUnicode.tools.jsonhelpers import json_path, json_to_file, dict_from_file



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
		self.unicodes_base        = set(uni_info.get("base", []))
		self.unicodes_optional    = set(uni_info.get("optional", [])) - self.unicodes_base
		self.unicodes_punctuation = set(uni_info.get("punctuation", []))
		
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
			parent = self._info().orthography(self.code, self.script)
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
	
	
	def support_full(self, cmap):
		if not self.scan_ok:
			self.scan_cmap(cmap)
		if self.num_missing_base == 0 and self.num_missing_optional == 0 and self.num_missing_punctuation == 0:
			return True
		return False
	
	
	def support_basic(self, cmap):
		if not self.scan_ok:
			self.scan_cmap(cmap)
		if self.num_missing_base == 0 and self.num_missing_punctuation == 0:
			return True
		return False
	
	
	def support_minimal(self, cmap):
		if not self.scan_ok:
			self.scan_cmap(cmap)
		if self.num_missing_base == 0 and self.num_missing_optional != 0 and self.num_missing_punctuation != 0:
			return True
		return False
	
	
	def almost_supported(self, cmap, max_missing = 5):
		if not self.scan_ok:
			self.scan_cmap(cmap)
		if 0 < self.num_missing_all <= max_missing:
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
	
	
	def scan_cmap(self, cmap):
		cmap_set = set(cmap)
		# Check for missing chars
		self.missing_base        = self.unicodes_base        - cmap_set
		self.missing_optional    = self.unicodes_optional    - cmap_set
		self.missing_punctuation = self.unicodes_punctuation - cmap_set
		self.missing_all = self.missing_base or self.missing_optional or self.missing_punctuation
		
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
		return self._info()
	
	
	@property
	def name(self):
		return self._name
		#if self.territory == "dflt":
		#	if self.script == "DFLT":
		#		return self._name
		#	else:
		#		return "%s (%s)" % (
		#			self._name,
		#			self.info.get_script_name(self.script),
		#		)
		#else:
		#	if self.script == "DFLT":
		#		return "%s (%s)" % (
		#			self._name,
		#			self.info.get_territory_name(self.territory),
		#		)
		#	else:
		#		return "%s (%s, %s)" % (
		#			self._name,
		#			self.info.get_script_name(self.script),
		#			self.info.get_territory_name(self.territory),
		#		)
	
	
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
		
		self._reverse_cmap = {}
	
	
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
	
	def scan_cmap(self, cmap):
		# Check the supplied cmap with all orthographies. This speeds up later operations.
		for o in self.orthographies:
			o.scan_cmap(cmap)
	
	
	def list_supported_orthographies(self, cmap, full_only=True):
		# Get a list of supported orthographies for a character list.
		result = []
		for o in self.orthographies:
			if full_only:
				if o.support_full(cmap):
					result.append(o)
			else:
				if o.support_basic(cmap):
					result.append(o)
		return result
	
	
	def list_supported_orthographies_minimum(self, cmap):
		# Get a list of minimally supported orthographies for a character list.
		result = []
		for o in self.orthographies:
			if o.support_minimal(cmap):
				result.append(o)
		return result
	
	
	def report_almost_supported_orthographies(self, cmap, max_missing=5):
		result = {}
		for o in self.orthographies:
			if o.almost_supported(cmap, max_missing):
				result[o.name] = o.missing_all
		return result
	
	
	#def __getitem__(self, key):
	#	return self.orthographies[key]
	
	
	def __len__(self):
		return len(self.orthographies)
	
	
	def __repr__(self):
		return u"<OrthographyInfo with %i orthographies>" % len(self)



# Test functions

def test_scan():
	from time import time
	from fontTools.ttLib import TTFont
	from htmlGenerator.fonttools.sfnt import get_cmap
	from jkUnicode import get_expanded_glyph_list
	
	
	# Get a character map from a font to scan.
	cmap = get_cmap(TTFont("/Users/jens/Documents/Schriften/Hertz/Hertz-Book.ttf"))
	start = time()
	o = OrthographyInfo()
	print o
	
	
	# List known orthographies
	for ot in o.orthographies:
		print ot.name
	
	
	# Scan for full, base and minimal support of the font's cmap
	full = o.list_supported_orthographies(cmap, full_only=True)
	base = o.list_supported_orthographies(cmap, full_only=False)
	mini = o.list_supported_orthographies_minimum(cmap)
	stop = time()
	
	print "\nFull support:", len(full), "orthography" if len(base) == 1 else "orthographies"
	print ", ".join(full)
	
	base = [r for r in base if not r in full]
	print "\nBasic support:", len(base), "orthography" if len(base) == 1 else "orthographies"
	print ", ".join(base)
	
	mini = [r for r in mini if not r in full]
	print "\nMinimal support (no punctuation):", len(mini), "orthography" if len(mini) == 1 else "orthographies"
	print ", ".join(mini)
	
	# Timing information
	print stop - start
	
	
	# Output info about one orthography
	ot = o.orthography("en", "DFLT", "ZA")
	print "\nOrthography:", ot.name
	print list(ot.unicodes_base)
	
	
	# Scan the font again, but allow for a number of missing characters
	n = 3
	almost = o.report_almost_supported_orthographies(cmap, n)
	print "\nAlmost supported (max. %i missing)):" % n, len(almost), "orthography" if len(almost) == 1 else "orthographies"
	for name in sorted(almost.keys()):
		print name
		# get_expanded_glyph_list adds case mapping entries and AGLFN glyph names to the list
		glyphs = get_expanded_glyph_list(almost[name])
		print "   ", " ".join([g[1] for g in glyphs])


def test_reverse():
	from time import time
	
	print "Test of the Reverse CMAP functions"
	
	c = u"ö"
	o = OrthographyInfo()
	
	print "Build reverse CMAP:", 
	start = time()
	o.build_reverse_cmap()
	stop = time()
	d = (stop - start) * 1000
	print "%0.2f ms" % d
	
	u = ord(c)
	
	start = time()
	result = o.get_orthographies_for_unicode(u)
	stop = time()
	d = (stop - start) * 1000
	print "Use cached lookup:  %0.2f ms" % d
	
	start = time()
	result = o.get_orthographies_for_unicode_any(u)
	stop = time()
	d = (stop - start) * 1000
	print "Use uncached lookup: %0.2f ms" % d
	
	
	print u"'%s' is used in:" % c
	for ot in sorted(result):
		print "   ", ot.name



if __name__ == "__main__":
	#test_scan()
	test_reverse()