# jkUnicode

A Python module for Unicode, glyph name, and orthography information.

The orthography functions can be used via the command line script `ortho`. The Unicode info for one or more codepoints can be shown via the command `uniinfo`.

For using the module from inside Python, see the [docs](https://jkunicode.readthedocs.io/en/latest/).

## `uniinfo`

`uniinfo` – Show information about Unicode codepoints.

### Usage

`uniinfo [-h] codepoint [codepoint ...]`

Codepoints can be given in decimal (e.g. `7838`), hexadecimal (e.g. `0x1e9e`), or Unicode (`U+1E9E`) notation.


## `ortho`

`ortho` – Query fonts about orthographic support.

### Usage

`usage: ortho [-h] [-b] [-f] [-i] [-k] [-m] [-p] [-n NEAR_MISS] [-s SUPPORT] font [font ...]`

### Options

#### -b

`-b, --bcp47`

Output orthographies as BCP47 language subtags instead of friendly names.

#### -f

`-f | --full-only`

When called without any options, `ortho` will determine the orthographic support of the supplied font(s) by looking at the required characters for each orthography. The `-f` option only lists orthographies for which all required _and_ optional characters are present in the font.

##### Example

```
$ ortho ComicJens.ttf 
The font supports 104 orthographies:
Afrikaans
Albanian
Asu
Azeri
Basque
Bemba
Bena
Bosnian
Catalan
[...]
Zulu

$ ortho -f ComicJens.ttf
The font supports 98 orthographies:
Afrikaans
Albanian
Asu
Azeri
Basque
Bemba
Bena
Bosnian
Catalan
[...]
Zulu
```

#### -i

`-i | --minimum-inclusive`

Prints a list of orthographies for which at least all characters from the basic category are present in the font.

##### Example

```
$ ortho -i ComicJens-Italic.ttf
The font has minimal or better support for 123 orthographies:
Afrikaans
Albanian
Asu
Azeri
[...]
Zulu
```

#### -k

`k | --kill-list`

Output a list of letters that don't appear together in any supported orthography.

#### -m

`m | --minimum`

Report orthographies that have only basic support, i.e. no optional characters and no punctuation present.


#### -p

`-p | --punctuation`

Prints a list of orthographies for which all letter category characters are present in the font, but have missing punctuation category characters. For the missing characters, Unicode, glyph name, and Unicode name are reported.

##### Example

```
$ ortho -p ComicJens.ttf
Orthographies which can be supported by adding punctuation characters:

Scottish Gaelic
    0x204A	uni204A	Tironian Sign Et
```

#### -n

`-n NEAR_MISS | --near-miss NEAR_MISS`

Prints a list of orthographies which are lacking up to a number of NEAR_MISS characters to be supported. For the missing characters, Unicode, glyph name, and Unicode name are reported.

##### Example

```
$ ortho -n 1 ComicJens.ttf
Orthographies which can be supported with max. 1 additional character:

Breton
    0x02BC	uni02BC	Modifier Letter Apostrophe

Hawaiian
    0x02BB	uni02BB	Modifier Letter Turned Comma

Quechua
    0x02BC	uni02BC	Modifier Letter Apostrophe

Tongan
    0x02BB	uni02BB	Modifier Letter Turned Comma
```

#### -s

`-s SUPPORT | --support SUPPORT`

Prints a report of characters missing to support an orthography specified by the supplied BCP47 language subtag. For the missing characters, Unicode, glyph name, and Unicode name are reported. Interacts with the options `-m` and `-p` to only show missing required characters or missing punctuation.

##### Example

```
$ ortho -p -s gd ComicJens.ttf
Scottish Gaelic
    0x204A	uni204A	Tironian sign et

$ ortho -m -s agq ComicJens.ttf
ortho -s agq -m /Users/kuti/Documents/Schriften/Comic-Jens-Font/build/ComicJensFreePro-Regular.ttf
Aghem
    0x0186	uni0186	Latin capital letter Open O
    0x0190	uni0190	Latin capital letter Open E
    0x0197	uni0197	Latin capital letter I with stroke
    0x0244	uni0244	Latin capital letter U Bar
    0x0254	uni0254	Latin small letter open o
    0x025B	uni025B	Latin small letter open e
    0x0268	uni0268	Latin small letter i with stroke
    0x0289	uni0289	Latin small letter u bar
    0x0294	uni0294	Latin letter glottal stop
```