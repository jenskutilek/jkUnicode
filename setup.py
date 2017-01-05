#! /usr/bin/env python

from distutils.core import setup

setup(
	name = "jkUnicode",
	version = "1.1",
	description = "Unicode support libraries.",
	author = "Jens Kutilek",
	url = "http://www.kutilek.de/",
	packages = [
		"jkUnicode",
		"jkUnicode.fonttools",
		"jkUnicode.tools",
	],
	package_dir = {"": "lib"},
	package_data = {"": [
		"json/ignored.json",
		"json/language_characters.json",
		"json/languages.json",
		"json/scripts.json",
		#"json/tags.json",
		"json/territories.json",
	]},
	requires = [
		"fontTools",
	],
	scripts = [
		"scripts/ortho",
	],
)
