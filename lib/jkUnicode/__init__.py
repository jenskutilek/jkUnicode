#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uniName import uniName
from uniCat import uniCat
from uniCase import uniUpperCaseMapping, uniLowerCaseMapping

categoryName = {
	'Lu':	'Letter, Uppercase',
	'Ll':	'Letter, Lowercase',
	'Lt':	'Letter, Titlecase',
	'Lm':	'Letter, Modifier',
	'Lo':	'Letter, Other',
	'Mn':	'Mark, Nonspacing',
	'Mc':	'Mark, Spacing Combining',
	'Me':	'Mark, Enclosing',
	'Nd':	'Number, Decimal Digit',
	'Nl':	'Number, Letter',
	'No':	'Number, Other',
	'Pc':	'Punctuation, Connector',
	'Pd':	'Punctuation, Dash',
	'Ps':	'Punctuation, Open',
	'Pe':	'Punctuation, Close',
	'Pi':	'Punctuation, Initial quote (may behave like Ps or Pe depending on usage)',
	'Pf':	'Punctuation, Final quote (may behave like Ps or Pe depending on usage)',
	'Po':	'Punctuation, Other',
	'Sm':	'Symbol, Math',
	'Sc':	'Symbol, Currency',
	'Sk':	'Symbol, Modifier',
	'So':	'Symbol, Other',
	'Zs':	'Separator, Space',
	'Zl':	'Separator, Line',
	'Zp':	'Separator, Paragraph',
	'Cc':	'Other, Control',
	'Cf':	'Other, Format',
	'Cs':	'Other, Surrogate',
	'Co':	'Other, Private Use',
	'Cn':	'Other, Not Assigned',
}

def getUnicodeChar(code):
	if code < 0x10000:
		return unichr(code)
	else:
		return eval("u'\U%08X'" % code)

class UniInfo(object):
	def __init__(self, uni):
		self.unicode = uni
	
	@property
	def unicode(self):
		return self._unicode
	
	@unicode.setter
	def unicode(self, value):
		self._unicode = value
		self._name = uniName.get(self._unicode, None)
		if self._name is None:
			if 0xE000 <= self._unicode < 0xF8FF:
				self._name = "<Private Use #%i>" % (self._unicode - 0xe000)
			elif 0xD800 <= self._unicode < 0xDB7F:
				self._name = "<Non Private Use High Surrogate #%i>" % (self._unicode - 0xd8000)
			elif 0xDB80 <= self._unicode < 0xDBFF:
				self._name = "<Private Use High Surrogate #%i>" % (self._unicode - 0xdb80)
			elif 0xDC00 <= self._unicode < 0xDFFF:
				self._name = "<Low Surrogate #%i>" % (self._unicode - 0xdc00)
			else:
				self._name = "<undefined>"
		self._categoryShort = uniCat.get(self._unicode, "<undefined>")
		self._category = categoryName.get(self._categoryShort, "<undefined>")
		self._uc_mapping = uniUpperCaseMapping.get(self._unicode, None)
		self._lc_mapping = uniLowerCaseMapping.get(self._unicode, None)
	
	def __repr__(self):
		if self.unicode is None:
			s =    " Unicode: None"
		else:
			s =    " Unicode: 0x%04X (dec. %s)" % (self.unicode, self.unicode)
		s += "\n    Name: %s" % self.name
		s += "\nCategory: %s (%s)" % (self._categoryShort, self.category)
		return s
	
	@property
	def category(self):
		return self._category
	
	@property
	def char(self):
		return getUnicodeChar(self.unicode)
	
	@property
	def glyphname(self):
		from aglfn import getGlyphnameForUnicode
		return getGlyphnameForUnicode(self.unicode)
	
	@property
	def name(self):
		return self._name
	
	@property
	def lc_mapping(self):
		return self._lc_mapping
	
	@property
	def uc_mapping(self):
		return self._uc_mapping
	
	# deprecated methods
	
	def getName(self):
		print "DEPRECATED: jkUnicode.UniInfo.getName()"
		return self._name
	
	def getCategory(self):
		print "DEPRECATED: jkUnicode.UniInfo.getCategory()"
		return self._category


if __name__ == '__main__':
	print "\n*** Test of jkUnicode.UniInfo ***"
	for u in [9912, 80]:
		j = UniInfo(u)
		print "Repr.:"
		print j
		print "- " * 20
		print "             Name:", j.name
		print "       Glyph Name:", j.glyphname
		print "         Category:", j.category
		print "        Character:", j.char
		lc = j.lc_mapping
		print "Lowercase Mapping:", lc
		if lc is not None:
			j.unicode = lc
			print j
		print "-" * 40
	