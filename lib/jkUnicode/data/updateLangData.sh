#!/bin/sh
# Check the URL if it is still current:
# http://unicode.org/Public/cldr/
# There seems to be no stable URL for the current version.
curl -O http://unicode.org/Public/cldr/41/core.zip
#unzip core.zip -d core/