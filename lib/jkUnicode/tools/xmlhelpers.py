#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The dirty hacky stuff is outsourced into this file

from re import compile
from jkUnicode import getUnicodeChar

ur = compile("^u([0-9A-F]+)") # Regex to match unicode sequences, e.g. \u0302


class Buffer(object):
	def __init__(self, string=u""):
		self._str = string
	
	def add(self, value):
		self._str += value
	
	def clear(self):
		self._str = u""
	
	def flush(self):
		v = self.__get__()
		self.clear()
		return v
	
	def __add__(self, value):
		print "ADD"
		self._str += value
	
	def __bool__(self):
		print "BOOL"
		if self._str:
			return True
		return False
	
	def __get__(self):
		m = ur.search(self._str)
		if m:
			return getUnicodeChar(int(m.groups(0)[0], 16))
		else:
			return self._str
	
	def __len__(self):
		return len(self._str)
	
	def __repr__(self):
		return self._str


def filtered_char_list(xml_char_list, debug=False):
	# Filter backslashes and other peculiarities of the XML format from the character list
	if xml_char_list[0] == "[" and xml_char_list[-1] == "]":
		xml_char_list = xml_char_list[1:-1]
	else:
		print "ERROR: Character list string from XML was not wrapped in []."
		return []
	
	filtered = []
	in_escape = False
	in_uniesc = False
	buf = Buffer()
	
	for c in xml_char_list:
		if debug: print "Chunk: '%s', buffer:'%s'" % (c, buf)
		if c == "\\":
			if in_escape:
				if buf: filtered.append(buf.flush())
			else:
				in_escape = True
		elif c == "}":
			if in_escape:
				if buf: filtered.append(buf.flush())
				filtered.append(c)
				in_escape = False
		elif c == "{":
			if in_escape:
				filtered.append(c)
				in_escape = False
		elif c == " ":
			if buf: filtered.append(buf.flush())
			in_escape = False
		elif c == "-":
			if in_escape:
				if buf: filtered.append(buf.flush())
				filtered.append(c)
				in_escape = False
			else:
				#filtered.append("RANGE")
				pass
		else:
			if in_escape:
				buf.add(c)
			else:
				filtered.append(c)
				#buf.clear()
		if debug: print "New buffer: '%s'" % buf
	
	if buf: filtered.append(buf.flush())
	
	if debug: print filtered
	#return filtered
	return sorted(list(set(filtered)))


if __name__ == "__main__":
	lists = [
		#(u"[\\u200C\\u200D \\u200F A {A\\u0301} {E \\u0302} {ij} {a b c} 未-札 \\]]", [u'-', u'A', u'E', u']', u'a', u'c', u'i', u'j', u'\u0301', u'\u0302', u'\u200c', u'\u200d', u'\u200f', u'\u672a', u'\u672b', u'\u672c', u'\u672d'])
		#(u"[\\u200C\\u200D-\\u200F A {A\\u0301} {E \\u0302} {ij}{a b c} 未-札 \\]]", [u'u200C', u'u200D', u'u200F', u'A', u'A', u'u0301', u'E', u'u0302', u'i', u'j', u'a', u'b', u'c', u'\u672a', u'-\u672d', u']'])
		(u"[\- , ; \: ! ? . « » ( ) \[ \] \{ \}]", [u'!', u'(', u')', u',', u'-', u'.', u':', u';', u'?', u'[', u']', u'{', u'}', u'\xab', u'\xbb'])
		#u"[a á à â ǎ ā {a\\u1DC6}{a\\u1DC7} b ɓ c d e é è ê ě ē {e\\u1DC6}{e\\u1DC7} ɛ {ɛ\\u0301} {ɛ\\u0300} {ɛ\\u0302} {ɛ\\u030C} {ɛ\\u0304} {ɛ\\u1DC6}{ɛ\\u1DC7} f g h i í ì î ǐ ī {i\\u1DC6}{i\\u1DC7} j k l m n ń ǹ ŋ o ó ò ô ǒ ō {o\\u1DC6}{o\\u1DC7} ɔ {ɔ\\u0301} {ɔ\\u0300} {ɔ\\u0302} {ɔ\\u030C} {ɔ\\u0304} {ɔ\\u1DC6}{ɔ\\u1DC7} p r s t u ú ù û ǔ ū {u\\u1DC6}{u\\u1DC7} v w y z]"
		#u"[\\u0F7E ཿ ཀ {ཀ\\u0FB5} \\u0F90 {\\u0F90\\u0FB5} ཁ \\u0F91 ག {ག\\u0FB7} \\u0F92 {\\u0F92\\u0FB7} ང \\u0F94 ཅ \\u0F95 ཆ \\u0F96 ཇ \\u0F97 ཉ \\u0F99 ཊ \\u0F9A ཋ \\u0F9B ཌ {ཌ\\u0FB7} \\u0F9C {\\u0F9C\\u0FB7} ཎ \\u0F9E ཏ \\u0F9F ཐ \\u0FA0 ད {ད\\u0FB7} \\u0FA1 {\\u0FA1\\u0FB7} ན \\u0FA3 པ \\u0FA4 ཕ \\u0FA5 བ {བ\\u0FB7} \\u0FA6 {\\u0FA6\\u0FB7} མ \\u0FA8 ཙ \\u0FA9 ཚ \\u0FAA ཛ {ཛ\\u0FB7} \\u0FAB {\\u0FAB\\u0FB7} ཝ \\u0FAD \\u0FBA ཞ \\u0FAE ཟ \\u0FAF འ \\u0FB0 ཡ \\u0FB1 \\u0FBB ར ཪ \\u0FB2 \\u0FBC ལ \\u0FB3 ཤ \\u0FB4 ཥ \\u0FB5 ས \\u0FB6 ཧ \\u0FB7 ཨ \\u0FB8 \\u0F72 {\\u0F71\\u0F72} \\u0F80 {\\u0F71\\u0F80} \\,
		#u"未-札"
	]

	for cl, r in lists:
		ll = filtered_char_list(cl, True)
		print "Result:", ll
		if ll == r:
			print "OK"
		else:
			print "ERROR"