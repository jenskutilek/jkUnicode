import unittest
from jkUnicode.orthography import OrthographyInfo


class TestOrthography(unittest.TestCase):
    def test_scan(self):
        from time import time
        from fontTools.ttLib import TTFont

        font_path = "/Users/jens/Documents/Schriften/Hertz/Hertz-Book.ttf"

        print("Scanning font for orthographic support:")
        print(font_path)

        # Get a character map from a font to scan.
        cmap = TTFont(font_path).getBestCmap()
        start = time()
        o = OrthographyInfo()
        print(o)

        # List known orthographies
        for ot in sorted(o.orthographies):
            print(ot.name, ot.code)

        o.cmap = cmap

        # Scan for full, base and minimal support of the font's cmap
        full = o.get_supported_orthographies(full_only=True)
        base = o.get_supported_orthographies(full_only=False)
        mini = o.get_supported_orthographies_minimum()
        stop = time()

        print(
            "\nFull support:",
            len(full),
            "orthography" if len(base) == 1 else "orthographies",
        )
        print(", ".join([x.name for x in full]))

        base = [r for r in base if r not in full]
        print(
            "\nBasic support:",
            len(base),
            "orthography" if len(base) == 1 else "orthographies",
        )
        print(", ".join([x.name for x in base]))

        mini = [r for r in mini if r not in full]
        print(
            "\nMinimal support (no punctuation):",
            len(mini),
            "orthography" if len(mini) == 1 else "orthographies",
        )
        print(", ".join([x.name for x in mini]))

        # Timing information
        print(stop - start)

        # Output info about one orthography
        ot = o.orthography("en", "DFLT", "ZA")
        print("\nOrthography:", ot.name)
        print(list(ot.unicodes_base))

        # Scan the font again, but allow for a number of missing characters
        print
        n = 3
        o.report_near_misses(n)


    def test_reverse(self):
        from time import time

        print("\nTest of the Reverse CMAP functions")

        c = "ö"
        o = OrthographyInfo()

        print("\nBuild reverse CMAP:",)
        start = time()
        o.build_reverse_cmap()
        stop = time()
        d = (stop - start) * 1000
        print("%0.2f ms" % d)

        u = ord(c)

        start = time()
        result1 = o.get_orthographies_for_unicode(u)
        stop = time()
        d = (stop - start) * 1000
        print("Use cached lookup:  %0.2f ms" % d)

        start = time()
        result2 = o.get_orthographies_for_unicode_any(u)
        stop = time()
        d = (stop - start) * 1000
        print("Use uncached lookup: %0.2f ms" % d)

        print("'%s' is used in:" % c)
        for ot in sorted(result1):
            print("   ", ot.name)
