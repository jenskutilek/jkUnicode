# jkUnicode

Ein Python-Modul für Unicode-, Glyphnamen- und Orthografie-Informationen

## Basisdaten aktualisieren

Das Modul bezieht seine Informationen aus den offiziellen Daten des Unicode-Standards, der Unicode-CLDR (Common Local Data Repository) und Adobe-AGLFN. Diese Daten müssen erst in ein auf das Modul zugeschnittenes Format konvertiert werden. Dazu sind die Skripte da, die sich im Ordner `jkUnicode/tools` befinden.

### Unicode- und AGLFN-Daten

- `updateUniData.sh` – Download der aktuellen Unicode- und AGLFN-Dateien.
- `generatePyUniData.py` – Update der Python-Module auf Basis der Unicode- und AGLFN-Daten

### Sprachunterstützungsdaten

- `updateLangData.sh` – Download der aktuellen Daten aus dem Unicode-CLDR.
- `generateJsonLangData.py` – Konvertieren der Sprachdatenbank ins JSON-Format
- `generatePyLangData.py` – Update der Python-Module auf Basis der JSON-Daten

Die Skripte sollten in dieser Reihenfolge ausgeführt werden. Nach `generateJsonLangData.py` kann man in die Sprachdefinitionen eingreifen, indem man gewünschte JSON-Dateien aus dem Ordner `jkUnicode/json/languages`in den Ordner `jkUnicode/json/overrides` kopiert und editiert. Dateien in diesem Ordner haben im nächsten Schritt (`generatePyLangData.py`) Vorrang vor den Originaldateien.