# -*- coding: utf-8 -*-
# Jens 2016-10-17

# Copy of htmlGenerator.fonttools.sfnt

def get_cmap(font):
	# Get the preferred cmap subtable from a fontTools.ttLib.TTFont
	table = font["cmap"]
	
	cmap = {}
	cmapIDs = [(3,10), (0,3), (3,1)]
	for i in range(len(cmapIDs)):
		if font["cmap"].getcmap(cmapIDs[i][0], cmapIDs[i][1]):
			cmap = font["cmap"].getcmap(cmapIDs[i][0], cmapIDs[i][1]).cmap
			break
	if not cmap:
		print "ERROR extracting codepoints from font. Found neither CMAP (3, 10), (0, 3), nor (3, 1)."
	return cmap


def get_names(font):
	# Get the full name and PostScript name from a fontTools.ttLib.TTFont
	full_name = font["name"].getName(4, 3, 1, 0x409).string.decode("utf_16_be")
	ps_name   = font["name"].getName(6, 3, 1, 0x409).string.decode("utf_16_be")
	return full_name, ps_name
