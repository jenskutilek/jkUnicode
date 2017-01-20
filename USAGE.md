# jkUnicode

## Command Line Scripts

`ortho` – Query fonts about orthographic support.

### Usage

`ortho ortho [-h] [-f] [-p] [-n NEAR_MISS] font [font ...]`

### Options

#### -f

`-f | --full-only`

When called without any options, `ortho` will determine the orthographic support of the supplied font(s) by looking at the required characters for each orthography. The `-f` option only lists orthographies for which all required _and_ optional characters are present in the font.

#### Example

```
$ ortho ComicJens.ttf 
The font supports 104 orthographies:
Afrikaans
Albanian
Asu (Tanzania)
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
Asu (Tanzania)
Azeri
Basque
Bemba
Bena
Bosnian
Catalan
[...]
Zulu
```

#### -p

`-p | --punctuation`

Prints a list of orthographies for which all letter category characters are present in the font, but have missing punctuation category characters. For the missing characters, Unicode, glyph name, and Unicode name are reported.

#### Example

```
$ ortho -p ComicJens.ttf
Orthographies which can be supported by adding punctuation characters:

Scottish Gaelic
    0x204A	uni204A	Tironian Sign Et
```

#### -n

`-n NEAR_MISS | --near-miss NEAR_MISS`

Prints a list of orthographies which are lacking up to a number of NEAR_MISS characters to be supported. For the missing characters, Unicode, glyph name, and Unicode name are reported.

#### Example

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