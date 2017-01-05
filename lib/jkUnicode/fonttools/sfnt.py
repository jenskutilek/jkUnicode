# -*- coding: utf-8 -*-
# Jens 2016-10-17

def get_cmap(font):
	# Get the preferred cmap subtable from a fontTools.ttLib.TTFont
	table = font["cmap"]
	
	cmap = {}
	cmapIDs = [(3, 10), (0, 3), (3, 1)]
	for i in range(len(cmapIDs)):
		if table.getcmap(cmapIDs[i][0], cmapIDs[i][1]):
			cmap = table.getcmap(cmapIDs[i][0], cmapIDs[i][1]).cmap
			break
	if not cmap:
		print "ERROR extracting codepoints from font. Found neither CMAP (3, 10), (0, 3), nor (3, 1)."
	return cmap

