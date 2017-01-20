# -*- coding: utf-8 -*-
# Jens 2016-10-17

def get_cmap(font):
	# Get the preferred cmap subtable from a fontTools.ttLib.TTFont
	
	for platformID, encodingID in [(3, 10), (0, 3), (3, 1)]:
		cmapSubtable = font["cmap"].getcmap(platformID, encodingID)
		if cmapSubtable is not None:
			return cmapSubtable.cmap
	print "ERROR extracting codepoints from font. Found neither CMAP (3, 10), (0, 3), nor (3, 1)."
	return {}

