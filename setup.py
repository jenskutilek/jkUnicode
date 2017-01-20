#! /usr/bin/env python

from setuptools import setup

setup(
	name = "jkUnicode",
	version = "1.2.0",
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
	install_requires = [
		"fontTools",
	],
	scripts = [
		"scripts/ortho",
	],
	#entry_points = {
	#	"console_scripts": [
	#		"ortho_scan="
	#	],
	#},
)
