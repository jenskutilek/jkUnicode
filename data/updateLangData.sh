#!/bin/sh

# Check the URL if it is still current:
# http://unicode.org/Public/cldr/
# There seems to be no stable URL for the current version.
curl -O https://unicode.org/Public/cldr/47/core.zip
#unzip core.zip -d core/

# BCP 47 language subtags
curl -O https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry
