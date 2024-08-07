# Updating the base data

The module takes its information from the official data of the Unicode standard, the Unicode CLDR (Common Locale Data Repository), and Adobe’s AGLFN standard. If you wish to update or customize this data, you must install the package from source code.

The downloaded data from the official sources must be converted to a format that is useable with this module. Scripts are included in the source code to aid this conversion. They can be found in `data` and `data-scripts`.

## Unicode and AGLFN data

- `data/updateUniData.sh` – Download the current Unicode and AGLFN data.
- `data-scripts/generatePyUniData.py` – Update the Python module based on the downloaded data.

## Orthography data

- `data/updateLangData.sh` – Download of the Unicode CLDR data.
- `data-scripts/generateJsonLangData.py` – Convert the CLDR data to the JSON format.
- `data-scripts/generateHyperglotData.py` – Convert the Hyperglot data to the JSON format.
- `data-scripts/generatePyLangData.py` – Update the Python module based on the JSON data.

The scripts should be executed in the given order. Before running `generateJsonLangData.py`, you can customize the display names by editing `json/override_names.json`.

After running it, you can edit the orthography definitions by copying any desired JSON file from the folder `jkUnicode/json/languages` to `jkUnicode/json/overrides` and editing it. Any files in this folder will override the original files in the next step (`generatePyLangData.py`). The data is merged using Python’s `dict.update()` method, so you only need to include any keys actually containing changes in your override file. 

If you want to add a new language definition that doesn’t override an existing one, you must add it to the overrides folder, and also add its code and name to `languages_additional.json`.

Any languages without orthography information will be listed in `ignored_languages.json`. This file is informational only and is not used by `jkUnicode`.

If you want to ignore any characters globally when determining orthography support, add them to `json/ignored_characters.json`.
