# Updating the base data

The module takes its information from the official data of the Unicode standard, the Unicode CLDR (Common Local Data Repository), and Adobe’s AGLFN standard. When updating these data, they must be converted to a format that is useable with this module. Scripts are included in the source code to aid this conversion. They can be found in `lib/jkUnicode/data` and `lib/jkUnicode/data-scripts`.

## Unicode and AGLFN data

- `data/updateUniData.sh` – Download the current Unicode and AGLFN data.
- `data-scripts/generatePyUniData.py` – Update the Python module based on the downloaded data.

## Orthography data

- `data/updateLangData.sh` – Download of the Unicode CLDR data.
- `data-scripts/generateJsonLangData.py` – Convert the CLDR data to the JSON format.
- `data-scripts/generatePyLangData.py` – Update the Python module based on the JSON data.

The scripts should be executed in the given order. After running `generateJsonLangData.py`, you can edit the orthography definitions by copying any desired JSON file from the folder `jkUnicode/json/languages` to `jkUnicode/json/overrides` and editing it. Any files in this folder will override the original files in the next step (`generatePyLangData.py`).

If you want to add a new language definition that doesn’t override an existing one, you must add it to the overrides folder, and also add its code and name to `languages_additional.json`.

Any languages without orthography information will be listed in `ignored.json`. This file is informational only and is not used by `jkUnicode`.
