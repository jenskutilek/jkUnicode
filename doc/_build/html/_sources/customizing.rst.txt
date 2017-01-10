Customizing Module Data
=======================

The jkUnicode modules read their data from Python, text, and JSON files generated from the official data sources. You can update, customize, and partially override this data in order to adapt the module's behaviour to your needs.

Glyph Name and Unicode Character Data
-------------------------------------

To download the current version of the glyph name and Unicode character data from their original sources (unicode.org and Adobe's GitHub repository), run the shell script `updateUniData.sh` in the `tools` folder included in the source distribution of jkUnicode. This will download the text files `aglfn.txt`, `Blocks.txt`, and `UnicodeData.txt`.

The raw downloads must then be converted into Python modules using the script `generatePyUniData.py`.

Orthography Data
----------------

The orthography submodule is derived from the Unicode Common Locale Data Repository (CLDR). To download a zip file of the core data, you can use the shell script `updateLangData.sh` in the `tools` subfolder. As there seems to be no stable URL for the latest version of this data, you have to check on http://unicode.org/Public/cldr/ if the URL in the script is pointing to the desired version before running the script.

After downloading, the data is extracted into the `tools/core` subfolder.

This data must then be converted from XML into an initial JSON representation by running the script `generateJsonLangData.py`. This will fill the `json/languages` subfolder with language-specific files as well as generate some files in the `tools` folder:

`tools/ignored.json`
   A list of language codes for which no orthography data is available from the original sources.

`tools/languages.json`
   Mapping from language codes to language names. The keys in this file are also used to look up files in the `languages` and `overrides` subfolders. If you want to add your own language definitions via override files, add their codes and names to `tools/languages_additonal.json`, as the `languages.json` file will be overwritten when you run `generateJsonLangData.py` again.

`tools/languages_additional.json`
   Mapping from language codes to language names for languages that are not part of the original data, but that you have added yourself via override files in `json/overrides/`.

`tools/scripts.json`
   Mapping from script codes to script names. There are no override files for scripts. If you want to add a new script that isn't already defined (Klingon?), modify this file directly and remember that it will be overwritten when you run `generateJsonLangData.py`, so you have will have to add your changes again.

`tools/territories.json`
   Mapping from territory codes to territory names. There are no override files for territories. If you want to add your own territory, modify this file directly and remember it will be overwritten when you run `generateJsonLangData.py` again.

If you want to override any of the orthography definitions, place a modified copy of any file from the `json/languages` subfolder in the `json/overrides` subfolder. You can omit any key/value pairs which would be identical in the override folder, in order to have as little data duplication as possible. The character representation and the Unicode name of the character are included just for easier reading, they can be omitted from the override files and are not part of the final data.

When you have customized the definitions to your liking, run the script `generatePyLangData.py` to convert the data from the initial JSON representation to the final JSON representation. This will update the file `tools/language_characters.json`, which is directly used by the :py:class:`jkUnicode.orthography` module.

Some characters are ignored by default in all orthography definitions. There is currently no way to edit these, other than to directly change the list IGNORED_UNICODES in :py:class:`jkUnicode.orthography`. The list currently contains the minute and second characters (U+2032, U+2033), which appear in many language definitions in the CLDR, but are not contained in a lot of standard font glyph sets.