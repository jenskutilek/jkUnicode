import unittest
from jkUnicode.orthography import OrthographyInfo
from os.path import dirname, join


def get_font_path(filename="Empty-Regular.ttf"):
    return join(dirname(__file__), "data", filename)


def get_cmap():
    from fontTools.ttLib import TTFont

    return TTFont(get_font_path()).getBestCmap()


class TestOrthographyInfo(unittest.TestCase):
    def test_known_orthographies(self):
        o = OrthographyInfo()
        orthographies = [f"{ot.name}: {ot.code}" for ot in o.orthographies]
        assert orthographies == [
            "Afrikaans: af",
            "Aghem: agq",
            "Akan: ak",
            "Amharic: am",
            "Obolo: ann",
            "Arabic (Morocco): ar",
            "Arabic: ar",
            "Assamese: as",
            "Asu: asa",
            "Asturian: ast",
            "Azeri (Cyrillic): az",
            "Azeri: az",
            "Basaa: bas",
            "Belarusian: be",
            "Bemba: bem",
            "Bena: bez",
            "Bulgarian: bg",
            "Haryanvi: bgc",
            "Bhojpuri: bho",
            "Bambara: bm",
            "Bangla: bn",
            "Tibetan: bo",
            "Breton: br",
            "Bodo: brx",
            "Bosnian (Cyrillic): bs",
            "Bosnian: bs",
            "Catalan: ca",
            "Chakma: ccp",
            "Chechen: ce",
            "Cebuano: ceb",
            "Chiga: cgg",
            "Cherokee: chr",
            "Kurdish, Sorani: ckb",
            "Czech: cs",
            "Chuvash: cv",
            "Welsh: cy",
            "Danish: da",
            "Taita: dav",
            "German, Swiss High (Switzerland): de",
            "German: de",
            "Zarma: dje",
            "Dogri: doi",
            "Sorbian, Lower: dsb",
            "Duala: dua",
            "Jola-Fonyi: dyo",
            "Dzongkha: dz",
            "Embu: ebu",
            "Ewe: ee",
            "Greek: el",
            "English (South Africa): en",
            "English: en",
            "Esperanto: eo",
            "Spanish: es",
            "Estonian: et",
            "Basque: eu",
            "Ewondo: ewo",
            "Dari (Afghanistan): fa",
            "Persian: fa",
            "Fula (Adlam): ff",
            "Fula: ff",
            "Finnish: fi",
            "Filipino: fil",
            "Faroese: fo",
            "French, Canadian (Canada): fr",
            "French: fr",
            "Frisian, Northern: frr",
            "Friulian: fur",
            "Frisian, Western: fy",
            "Irish: ga",
            "Scottish Gaelic: gd",
            "Galician: gl",
            "German, Swiss: gsw",
            "Gujarati: gu",
            "Gusii: guz",
            "Manx: gv",
            "Hausa (Niger): ha",
            "Hausa: ha",
            "Hawaiian: haw",
            "Hebrew: he",
            "Hindi: hi",
            "Hinglish (Latin): hi",
            "Croatian: hr",
            "Sorbian, Upper: hsb",
            "Hungarian: hu",
            "Armenian: hy",
            "Interlingua: ia",
            "Indonesian: id",
            "Igbo: ig",
            "Sichuan Yi: ii",
            "International Phonetic Alphabet: ipa",
            "Icelandic: is",
            "Italian: it",
            "Japanese: ja",
            "Ngomba: jgo",
            "Machame: jmc",
            "Javanese: jv",
            "Georgian: ka",
            "Kabyle: kab",
            "Kamba: kam",
            "Makonde: kde",
            "Kabuverdianu: kea",
            "Kaingang: kgp",
            "Koyra Chiini: khq",
            "Kikuyu: ki",
            "Kazakh: kk",
            "Kako: kkj",
            "Kalaallisut: kl",
            "Kalenjin: kln",
            "Khmer: km",
            "Kannada: kn",
            "Korean: ko",
            "Konkani: kok",
            "Kashmiri: ks",
            "Kashmiri (Devanagari): ks",
            "Shambala: ksb",
            "Bafia: ksf",
            "Colognian: ksh",
            "Kurdish: ku",
            "Cornish: kw",
            "Kirghiz: ky",
            "Langi: lag",
            "Luxembourgish: lb",
            "Ganda: lg",
            "Lakota: lkt",
            "Lingala: ln",
            "Lao: lo",
            "Luri, Northern: lrc",
            "Lithuanian: lt",
            "Luba-Katanga: lu",
            "Luo: luo",
            "Luyia: luy",
            "Latvian: lv",
            "Maithili: mai",
            "Masai: mas",
            "Moksha: mdf",
            "Meru: mer",
            "Morisyen: mfe",
            "Malagasy: mg",
            "Makhuwa-Meetto: mgh",
            "Metaʼ: mgo",
            "Māori: mi",
            "Macedonian: mk",
            "Malayalam: ml",
            "Mongolian: mn",
            "Manipuri: mni",
            "Marathi: mr",
            "Malay: ms",
            "Maltese: mt",
            "Mundang: mua",
            "Myanmar Language: my",
            "Mazanderani: mzn",
            "Nama: naq",
            "Ndebele, North: nd",
            "Saxon, Low (Netherlands): nds",
            "German, Low: nds",
            "Nepali: ne",
            "Dutch: nl",
            "Kwasio: nmg",
            "Norwegian Nynorsk: nn",
            "Ngiemboon: nnh",
            "Norwegian: no",
            "Nuer: nus",
            "Nyankole: nyn",
            "Occitan (Spain): oc",
            "Occitan: oc",
            "Oromo: om",
            "Odia: or",
            "Ossetic: os",
            "Punjabi (Perso-Arabic): pa",
            "Punjabi: pa",
            "Pidgin, Nigerian: pcm",
            "Pijin: pis",
            "Polish: pl",
            "Pushto (Pakistan): ps",
            "Pushto: ps",
            "Portuguese, European (Portugal): pt",
            "Portuguese: pt",
            "Quechua: qu",
            "Rajasthani: raj",
            "Romansh: rm",
            "Rundi: rn",
            "Romanian: ro",
            "Rombo: rof",
            "Russian: ru",
            "Kinyarwanda: rw",
            "Rwa: rwk",
            "Sanskrit: sa",
            "Yakut: sah",
            "Samburu: saq",
            "Santali: sat",
            "Sangu: sbp",
            "Sardinian: sc",
            "Sindhi: sd",
            "Sindhi (Devanagari): sd",
            "Sami, Northern: se",
            "Sena: seh",
            "Koyraboro Senni: ses",
            "Sango: sg",
            "Tachelhit: shi",
            "Tachelhit (Latin): shi",
            "Sinhala: si",
            "Slovak: sk",
            "Slovenian: sl",
            "Sami, Inari: smn",
            "Sami, Skolt: sms",
            "Shona: sn",
            "Somali: so",
            "Albanian: sq",
            "Serbian: sr",
            "Serbian (Latin): sr",
            "Sundanese: su",
            "Swedish: sv",
            "Swahili, Congo (Congo (DRC)): sw",
            "Swahili (Kenya): sw",
            "Swahili: sw",
            "Tamil: ta",
            "Telugu: te",
            "Teso: teo",
            "Tajik: tg",
            "Thai: th",
            "Tigrinya (Eritrea): ti",
            "Tigrinya: ti",
            "Turkmen: tk",
            "Tongan: to",
            "Toki Pona: tok",
            "Turkish: tr",
            "Tatar: tt",
            "Tasawaq: twq",
            "Tamazight, Central Atlas: tzm",
            "Uighur: ug",
            "Ukrainian: uk",
            "Urdu: ur",
            "Uzbek (Perso-Arabic): uz",
            "Uzbek (Cyrillic): uz",
            "Uzbek: uz",
            "Vai: vai",
            "Vai (Latin): vai",
            "Vietnamese: vi",
            "Vunjo: vun",
            "Walser: wae",
            "Wolof: wo",
            "Xhosa: xh",
            "Soga: xog",
            "Yangben: yav",
            "Yiddish: yi",
            "Yoruba (Benin): yo",
            "Yoruba: yo",
            "Nheengatu: yrl",
            "Chinese, Cantonese: yue",
            "Chinese, Cantonese (Simplified Han): yue",
            "Tamazight, Standard Moroccan: zgh",
            "Chinese, Mandarin: zh",
            "Chinese, Traditional Mandarin (Traditional Han): zh",
            "Zulu: zu",
        ]

    def test_scan_full(self):
        o = OrthographyInfo()
        o.cmap = get_cmap()
        supported = o.get_supported_orthographies(full_only=True)
        orthographies = [f"{ot.name}: {ot.code}" for ot in supported]
        assert orthographies == [
            "Asu: asa",
            "Bemba: bem",
            "Bena: bez",
            "Chiga: cgg",
            "Taita: dav",
            "Jola-Fonyi: dyo",
            "Embu: ebu",
            "Friulian: fur",
            "Gusii: guz",
            "Machame: jmc",
            "Javanese: jv",
            "Kamba: kam",
            "Makonde: kde",
            "Kikuyu: ki",
            "Kalenjin: kln",
            "Shambala: ksb",
            "Cornish: kw",
            "Ganda: lg",
            "Luo: luo",
            "Luyia: luy",
            "Meru: mer",
            "Morisyen: mfe",
            "Malagasy: mg",
            "Makhuwa-Meetto: mgh",
            "Māori: mi",
            "Ndebele, North: nd",
            "Nyankole: nyn",
            "Oromo: om",
            "Rundi: rn",
            "Rombo: rof",
            "Kinyarwanda: rw",
            "Rwa: rwk",
            "Samburu: saq",
            "Sangu: sbp",
            "Sami, Northern: se",
            "Sena: seh",
            "Sango: sg",
            "Sami, Inari: smn",
            "Shona: sn",
            "Teso: teo",
            "Vunjo: vun",
            "Soga: xog",
        ]

    def test_scan_base(self):
        o = OrthographyInfo()
        o.cmap = get_cmap()
        supported = o.get_supported_orthographies(full_only=False)
        orthographies = [f"{ot.name}: {ot.code}" for ot in supported]
        assert orthographies == [
            "Asu: asa",
            "Bemba: bem",
            "Bena: bez",
            "Chiga: cgg",
            "Taita: dav",
            "Jola-Fonyi: dyo",
            "Embu: ebu",
            "Friulian: fur",
            "German, Swiss: gsw",
            "Gusii: guz",
            "Hinglish (Latin): hi",
            "Machame: jmc",
            "Javanese: jv",
            "Kamba: kam",
            "Makonde: kde",
            "Kikuyu: ki",
            "Kalaallisut: kl",
            "Kalenjin: kln",
            "Shambala: ksb",
            "Cornish: kw",
            "Ganda: lg",
            "Luo: luo",
            "Luyia: luy",
            "Meru: mer",
            "Morisyen: mfe",
            "Malagasy: mg",
            "Makhuwa-Meetto: mgh",
            "Māori: mi",
            "Ndebele, North: nd",
            "Norwegian Nynorsk: nn",
            "Nyankole: nyn",
            "Oromo: om",
            "Romansh: rm",
            "Rundi: rn",
            "Rombo: rof",
            "Kinyarwanda: rw",
            "Rwa: rwk",
            "Samburu: saq",
            "Sangu: sbp",
            "Sami, Northern: se",
            "Sena: seh",
            "Sango: sg",
            "Sami, Inari: smn",
            "Shona: sn",
            "Teso: teo",
            "Vunjo: vun",
            "Walser: wae",
            "Soga: xog",
        ]

    def test_scan_minimal(self):
        o = OrthographyInfo()
        o.cmap = get_cmap()
        supported = o.get_supported_orthographies_minimum()
        orthographies = [f"{ot.name}: {ot.code}" for ot in supported]
        assert orthographies == [
            "Breton: br",
            "Czech: cs",
            "Welsh: cy",
            "Danish: da",
            "German, Swiss High (Switzerland): de",
            "German: de",
            "Sorbian, Lower: dsb",
            "English (South Africa): en",
            "English: en",
            "Spanish: es",
            "Estonian: et",
            "Basque: eu",
            "Finnish: fi",
            "French, Canadian (Canada): fr",
            "French: fr",
            "Frisian, Northern: frr",
            "Irish: ga",
            "Scottish Gaelic: gd",
            "Galician: gl",
            "Sorbian, Upper: hsb",
            "Hungarian: hu",
            "Interlingua: ia",
            "Indonesian: id",
            "Italian: it",
            "Kabuverdianu: kea",
            "Kaingang: kgp",
            "Colognian: ksh",
            "Kurdish: ku",
            "Luxembourgish: lb",
            "German, Low: nds",
            "Norwegian: no",
            "Occitan (Spain): oc",
            "Occitan: oc",
            "Portuguese, European (Portugal): pt",
            "Portuguese: pt",
            "Quechua: qu",
            "Sardinian: sc",
            "Slovak: sk",
            "Slovenian: sl",
            "Sundanese: su",
            "Turkish: tr",
            "Xhosa: xh",
            "Nheengatu: yrl",
            "Zulu: zu",
        ]

    def test_almost_supported(self):
        # Check which orthographies are missing at most 3 characters
        o = OrthographyInfo()
        o.cmap = get_cmap()
        supported = o.get_almost_supported(3)
        orthographies = [f"{ot.name}: {ot.code}" for ot in supported]
        assert orthographies == [
            "Obolo: ann",
            "Catalan: ca",
            "Zarma: dje",
            "Hawaiian: haw",
            "Igbo: ig",
            "Koyra Chiini: khq",
            "Lakota: lkt",
            "Metaʼ: mgo",
            "Koyraboro Senni: ses",
            "Tongan: to",
            "Tasawaq: twq",
            "Uzbek: uz",
        ]

    def test_get_missing(self):
        o = OrthographyInfo()
        o.cmap = get_cmap()
        ot = o.orthography("de", territory="CH")
        assert ot is not None

        missing = ot.get_missing(minimum=False, punctuation=False)
        characters = sorted(missing)
        assert characters == [
            33,
            34,
            35,
            38,
            39,
            40,
            41,
            42,
            47,
            58,
            59,
            63,
            64,
            91,
            93,
            123,
            125,
            167,
            171,
            187,
            276,
            277,
            300,
            301,
            334,
            335,
            8211,
            8212,
            8216,
            8218,
            8220,
            8222,
            8230,
        ]

    def test_get_missing_minimum(self):
        o = OrthographyInfo()
        o.cmap = get_cmap()
        ot = o.orthography("agq")
        assert ot is not None

        missing = ot.get_missing(minimum=True, punctuation=False)
        characters = sorted(missing)
        print(characters)
        assert characters == [
            390,
            400,
            407,
            461,
            462,
            463,
            464,
            465,
            466,
            467,
            468,
            580,
            596,
            603,
            616,
            649,
            660,
        ]

    def test_get_missing_punctuation(self):
        o = OrthographyInfo()
        o.cmap = get_cmap()
        ot = o.orthography("de", territory="CH")
        assert ot is not None

        missing = ot.get_missing(minimum=False, punctuation=True)
        characters = sorted(missing)
        assert characters == [
            33,
            34,
            35,
            38,
            39,
            40,
            41,
            42,
            47,
            58,
            59,
            63,
            64,
            91,
            93,
            123,
            125,
            167,
            171,
            187,
            8211,
            8212,
            8216,
            8218,
            8220,
            8222,
            8230,
        ]

    def test_get_missing_unknown(self):
        o = OrthographyInfo()
        o.cmap = get_cmap()
        ot = o.orthography("jens")
        assert ot is None

    def test_single_orthography(self):
        # Info about one orthography
        o = OrthographyInfo()
        ot = o.orthography("en", "DFLT", "ZA")
        assert ot is not None
        assert ot.name == "English (South Africa)"
        assert ot.unicodes_base == {
            65,
            66,
            67,
            68,
            69,
            70,
            71,
            72,
            73,
            74,
            75,
            76,
            77,
            78,
            79,
            80,
            81,
            82,
            83,
            84,
            85,
            86,
            87,
            88,
            89,
            90,
            97,
            98,
            99,
            100,
            101,
            102,
            103,
            104,
            105,
            106,
            107,
            108,
            109,
            110,
            111,
            112,
            113,
            114,
            115,
            116,
            117,
            118,
            119,
            120,
            121,
            122,
        }

    def test_reverse(self):
        """
        Get orthographies that support a given codepoint.
        """
        o = OrthographyInfo()
        o.build_reverse_cmap()
        u = ord("ö")
        result1 = [ot.code for ot in o.get_orthographies_for_unicode(u)]
        assert result1 == [
            "af",
            "az",
            "cy",
            "de",
            "de",
            "et",
            "fi",
            "frr",
            "fy",
            "gsw",
            "hu",
            "is",
            "ksh",
            "nds",
            "nl",
            "nmg",
            "nus",
            "sg",
            "sv",
            "tk",
            "tr",
            "wae",
        ]

        result2 = [ot.code for ot in o.get_orthographies_for_unicode_any(u)]
        assert result2 == [
            "af",
            "ast",
            "az",
            "br",
            "ca",
            "cs",
            "cy",
            "da",
            "de",
            "de",
            "dsb",
            "ee",
            "en",
            "en",
            "es",
            "et",
            "eu",
            "fi",
            "fr",
            "fr",
            "frr",
            "fy",
            "gd",
            "gl",
            "gsw",
            "hsb",
            "hu",
            "ia",
            "id",
            "is",
            "it",
            "kea",
            "kgp",
            "ksh",
            "lb",
            "nds",
            "nds",
            "nl",
            "nmg",
            "nn",
            "no",
            "nus",
            "oc",
            "pl",
            "pt",
            "qu",
            "rm",
            "ro",
            "sc",
            "se",
            "sg",
            "sk",
            "sl",
            "smn",
            "sms",
            "su",
            "sv",
            "tk",
            "to",
            "tr",
            "uz",
            "wae",
            "xh",
            "yrl",
            "zu",
        ]
