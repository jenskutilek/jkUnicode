# Changelog

## v2.7.1

- Update Unicode data to v18 and CLDR data to v48.2
- Bring back Python 3.11, add Python 3.15
- Remove codecs module from data scripts
- Update dependencies
- Fix path in data scripts
- Add more typing and tests

## v2.6.0

- Add `--meta` argument to `ortho` command line script
- Return `set` instead of `lists` where it makes sense
- Make Orthography objects hashable
- Use logging for warnings instead of print
- Add more proper tests
- Apply ruff suggestions
- Update uharfbuzz, sphinx

```bash
ortho --meta font [font ...]
```

Output a meta table in YAML format. Ignores most other options. Orthographies with full
support are listed under the `dlng` (design languages) key, and orthographies with
basic support are listed under the `slng` (supported languages) key. You will most
certainly not warnt to rely on this classification to build a meta table for a font
directly, as the tool has no way of detecting actual fitness for typesetting a certain
orthography.

Example:

```bash
ortho --meta myfont.ttf
meta:
  dlng:
    - "sq" # Albanian
    - "az" # Azeri
    - "bs" # Bosnian
    # ...
  slng:
    - "trv" # Taroko
```

## v2.5.0

- Modernize: build package with uv
- Update to Hyperglot v0.8.1
- Drop Python 3.10, 3.11 support
- Remove deprecated codecs package
