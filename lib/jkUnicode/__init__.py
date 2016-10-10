from uniName import uniName
from uniCat import uniCat

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
		if uniName.has_key(self.unicode):
			self.name = uniName[self.unicode]
		else:
			if 0xE000 <= self.unicode < 0xF8FF:
				self.name = "<Private Use #%i>" % (self.unicode - 0xe000)
			elif 0xD800 <= self.unicode < 0xDB7F:
				self.name = "<Non Private Use High Surrogate #%i>" % (self.unicode - 0xd8000)
			elif 0xDB80 <= self.unicode < 0xDBFF:
				self.name = "<Private Use High Surrogate #%i>" % (self.unicode - 0xdb80)
			elif 0xDC00 <= self.unicode < 0xDFFF:
				self.name = "<Low Surrogate #%i>" % (self.unicode - 0xdc00)
			else:
				self.name = "<undefined>"
		if uniCat.has_key(self.unicode):
			self.categoryShort = uniCat[self.unicode]
			self.category = categoryName[self.categoryShort]
		else:
			self.categoryShort = "<undefined>"
			self.category = "<undefined>"
	
	def __str__(self):
		s =    " Unicode: " + hex(self.unicode) + " (dec. " + str(self.unicode) + ")"
		s += "\n    Name: " + self.name
		s += "\nCategory: " + self.categoryShort + " (" + self.category + ")"
		return s
	
	def getName(self):
		return self.name
	
	def getCategory(self):
		return self.category
	


if __name__ == '__main__':
	print "\n*** Test of jkUnicode.UniInfo ***"
	j = jkUniInfo(9912)
	print "Repr.:"
	print j
	print "\ngetName:"
	print j.getName()
	print "\ngetCategory:"
	print j.getCategory()