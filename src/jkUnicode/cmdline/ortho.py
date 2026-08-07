import argparse
from sys import exit

try:
    from fontTools.ttLib import TTFont
except ImportError:
    print(
        "Please install the jkUnicode Python package with the 'sfnt' or 'woff' extras "
        "to use this command."
    )
    exit(1)

from jkUnicode.orthography import OrthographyInfo


class OrthoCmdLine:
    def __init__(self, font_path: str, args: argparse.Namespace) -> None:
        self.o = OrthographyInfo(source=args.source[0])
        cmap = self.get_cmap(font_path)
        if cmap is None:
            print("No suitable cmap table was found in the font.")
            exit(1)

        self.o.cmap = cmap
        if args.meta:
            meta = "meta:\n"

            dlng = self.o.get_supported_orthographies(full_only=True)
            fully_supported = []
            for o in sorted(dlng):
                fully_supported.append(f'    - "{o.identifier}" # {o.name}')
            if fully_supported:
                meta += "  dlng:\n" + "\n".join(fully_supported) + "\n"

            slng = self.o.get_supported_orthographies(full_only=False)
            basic_supported = []
            for o in sorted(slng):
                if o in dlng:
                    continue
                basic_supported.append(f'.   - "{o.identifier}" # {o.name}')
            if basic_supported:
                meta += "  slng:\n" + "\n".join(basic_supported) + "\n"

            print(meta)
        elif args.support:
            self.o.report_missing(
                codes=args.support,
                minimum=args.minimum,
                punctuation=args.punctuation,
                bcp47=args.bcp47,
            )
        elif args.punctuation:
            self.o.report_missing_punctuation(bcp47=args.bcp47)
        elif args.near_miss:
            self.o.report_near_misses(args.near_miss[0], bcp47=args.bcp47)
        elif args.minimum:
            self.o.report_supported_minimum(bcp47=args.bcp47)
        elif args.minimum_inclusive:
            self.o.report_supported_minimum_inclusive(bcp47=args.bcp47)
        elif args.full_only:
            self.o.report_supported(full_only=True, bcp47=args.bcp47)
        elif args.kill_list:
            self.o.report_kern_list(bcp47=args.bcp47, include_optional=False)
        else:
            self.o.report_supported(full_only=False, bcp47=args.bcp47)

    def get_cmap(self, font_path: str) -> dict[int, str] | None:
        # Get a cmap from a given font path
        f = TTFont(font_path)
        cmap = f.getBestCmap()
        f.close()
        return cmap


def ortho() -> None:
    parser = argparse.ArgumentParser(
        description="Query fonts about orthographic support."
    )
    parser.add_argument(
        "-b",
        "--bcp47",
        action="store_true",
        default=False,
        help="Output orthographies as BCP47 language subtags",
    )
    parser.add_argument(
        "-f",
        "--full-only",
        action="store_true",
        default=False,
        help=(
            "Report only orthographies that are supported with all optional characters"
        ),
    )
    parser.add_argument(
        "-i",
        "--minimum-inclusive",
        action="store_true",
        default=False,
        help="Report orthographies that have at minimum basic support",
    )
    parser.add_argument(
        "-k",
        "--kill-list",
        action="store_true",
        default=False,
        help=(
            "Output a list of letters that don't appear together in any supported "
            "orthography."
        ),
    )
    parser.add_argument(
        "-m",
        "--minimum",
        action="store_true",
        default=False,
        help=(
            "Report orthographies that have only basic support, i.e. no optional "
            "characters and no punctuation present"
        ),
    )
    parser.add_argument(
        "--meta",
        action="store_true",
        default=False,
        help="Output a meta table in YAML format. Ignores most other options.",
    )
    parser.add_argument(
        "-p",
        "--punctuation",
        action="store_true",
        default=False,
        help="Report missing punctuation for otherwise supported orthographies",
    )
    parser.add_argument(
        "-n",
        "--near-miss",
        type=int,
        nargs=1,
        help=(
            "Report almost supported orthographies with maximum number of missing "
            "characters"
        ),
    )
    parser.add_argument(
        "-s",
        "--support",
        type=str,
        nargs=1,
        help=(
            "List Unicode characters missing from font to support the provided BCP47 "
            "language code"
        ),
    )
    parser.add_argument(
        "--source",
        type=str,
        default=["CLDR"],
        nargs=1,
        help=("Specify the source of orthography data, CLDR (default) or Hyperglot"),
    )
    parser.add_argument("font", type=str, nargs="+", help="One or more fonts")

    args = parser.parse_args()

    for font_path in args.font:
        OrthoCmdLine(font_path, args)


if __name__ == "__main__":
    ortho()
