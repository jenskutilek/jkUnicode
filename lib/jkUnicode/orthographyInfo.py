#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os
from jkUnicode.tools.jsonhelpers import json_path, json_to_file, dict_from_file


class Orthography(object):
	
	def __init__(self, info_dict):
		self.from_dict(info_dict)
	
	
	def from_dict(self, info_dict):
		#self.code = info_dict.get("code", None)
		self.name = info_dict.get("name", None)
		uni_info = info_dict.get("unicodes", {})
		self.unicodes_base        = set(uni_info.get("base", []))
		self.unicodes_optional    = set(uni_info.get("optional", []))
		self.unicodes_punctuation = set(uni_info.get("punctuation", []))
		self.scan_ok = False
	
	
	def support_full(self, cmap):
		if not self.scan_ok:
			self.scan_cmap(cmap)
		if self.num_missing_base == 0 and self.num_missing_optional == 0 and self.num_missing_punctuation == 0:
			return True
		return False
	
	
	def support_basic(self, cmap):
		if not self.scan_ok:
			self.scan_cmap(cmap)
		if self.num_missing_base == 0 and self.num_missing_optional != 0 and self.num_missing_punctuation == 0:
			return True
		return False
	
	
	def support_minimal(self, cmap):
		if not self.scan_ok:
			self.scan_cmap(cmap)
		if self.num_missing_base == 0 and self.num_missing_optional != 0 and self.num_missing_punctuation != 0:
			return True
		return False
	
	
	def scan_cmap(self, cmap):
		cmap_set = set(cmap)
		# Check for missing chars
		self.missing_base        = self.unicodes_base        - cmap_set
		self.missing_optional    = self.unicodes_optional    - cmap_set
		self.missing_punctuation = self.unicodes_punctuation - cmap_set
		
		self.num_missing_base        = len(self.missing_base)
		self.num_missing_optional    = len(self.missing_optional)
		self.num_missing_punctuation = len(self.missing_punctuation)
		
		# Calculate percentage
		self.base_pc        = 1 - self.num_missing_base / len(self.unicodes_base) if self.unicodes_base else 0
		self.optional_pc    = 1 - self.num_missing_optional / len(self.unicodes_optional) if self.unicodes_optional else 0
		self.punctuation_pc = 1 - self.num_missing_punctuation / len(self.unicodes_punctuation) if self.unicodes_punctuation else 0
	
	
	def forget_cmap(self):
		self.scan_ok = False
	
	def __repr__(self):
		return u'<Orthography "%s">' % self.name

class OrthographyInfo(object):
	def __init__(self):
		data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "json")
		language_chars_dict = dict_from_file(data_path, "language_characters")
		self.orthographies = {code: Orthography(info) for code, info in language_chars_dict.items()}
	
	def orthography(self, code):
		return self.orthographies[code]
	
	def scan_cmap(self, cmap):
		result = {c: o.scan_cmap(cmap) for c, o in self.orthographies.items()}
		return result
	
	def list_supported_orthographies(self, cmap, full_only=True):
		result = []
		for c, o in self.orthographies.items():
			if full_only:
				if o.support_full(cmap):
					result.append(o.name)
			else:
				if o.support_basic(cmap):
					result.append(o.name)
		return result
	
	def list_supported_orthographies_minimum(self, cmap):
		result = []
		for c, o in self.orthographies.items():
			if o.support_minimal(cmap):
				result.append(o.name)
		return result
	
	def __len__(self):
		return len(self.orthographies)
	
	def __repr__(self):
		return u"<OrthographyInfo with %i orthographies>\n" % len(self)


def test_scan():
	from time import time
	from fontTools.ttLib import TTFont
	from htmlGenerator.fonttools.sfnt import get_cmap
	cmap = get_cmap(TTFont("/Users/jens/Code/HTMLGenerator/Lib/testdata/consola.ttf"))
	start = time()
	o = OrthographyInfo()
	full = o.list_supported_orthographies(cmap, full_only=True)
	base = o.list_supported_orthographies(cmap, full_only=False)
	mini = o.list_supported_orthographies_minimum(cmap)
	stop = time()
	print "\nFull support:", len(full), "orthography" if len(base) == 1 else "orthographies"
	print ", ".join(sorted(full))
	base = [r for r in base if not r in full]
	print "\nBasic support:", len(base), "orthography" if len(base) == 1 else "orthographies"
	print ", ".join(sorted(base))
	mini = [r for r in mini if not r in full]
	print "\nMinimal support (no punctuation):", len(mini), "orthography" if len(mini) == 1 else "orthographies"
	print ", ".join(sorted(mini))
	print stop - start


if __name__ == "__main__":
	#o = OrthographyInfo()
	#print o
	test_scan()