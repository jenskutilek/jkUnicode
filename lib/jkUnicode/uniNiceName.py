import re

#re_small_letter   = re.compile("^(.+SMALL LETTER )([A-Z ]+?)( WITH.+)?$")
re_capital_letter = re.compile("^(.+CAPITAL LETTER )([A-Z ]+?)( WITH.+)?$")
re_allah = re.compile("^(.+?)(ALLAH)(.+)?$")

letter_names = {
	"AE": "AE",
}

#def transform_small_letter(name):
#	#print "transform_small_letter", name
#	m = re_small_letter.match(name)
#	if m:
#		#print m.groups()
#		result = "%s%s" % (m.group(1).capitalize(), str(m.group(2)).lower())
#		if m.group(3) is not None:
#			result += "%s" % m.group(3).lower()
#		#print "Result:", result
#		return result
#	return False

def transform_capital_letter(name):
	#print "transform_capital_letter", name
	m = re_capital_letter.match(name)
	if m:
		#print m.groups()
		result = "%s%s" % (m.group(1).capitalize(), letter_names.get(m.group(2), m.group(2).title()))
		if m.group(3) is not None:
			result += "%s" % m.group(3).lower()
		#print "Result:", result
		return result
	return False

def transform_allah(name):
	m = re_allah.match(name)
	if m:
		result = "%s%s" % (m.group(1).capitalize(), m.group(2).title())
		if m.group(3) is not None:
			result += "%s" % m.group(3).lower()
		print result
		return result
	return False


nice_name_rules = [
	#transform_small_letter,
	transform_capital_letter,
	transform_allah,
]
