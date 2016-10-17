#! /usr/bin/env python

from distutils.core import setup

setup(
		name = "jkUnicode",
		version = "1.0",
		description = "Unicode support libraries.",
		author = "Jens Kutilek",
		url = "http://www.kutilek.de/",
		packages = [
			"jkUnicode",
			#"jkUnicode.tools",
		],
		package_dir = {"": "lib"},
	)
