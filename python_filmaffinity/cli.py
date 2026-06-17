"""Command line interface for python-filmaffinity."""

import argparse
import sys

from . import FilmAffinity, to_json


TOP_METHODS = {
    "filmaffinity": "top_filmaffinity",
    "tv_series": "top_tv_series",
    "premieres": "top_premieres",
    "dvd": "top_dvd",
    "netflix": "top_netflix",
    "hbo": "top_hbo",
    "filmin": "top_filmin",
    "movistar": "top_movistar",
    "rakuten": "top_rakuten",
}


def _build_service(args):
    return FilmAffinity(lang=args.lang, cache_backend=args.cache_backend)


def _as_rows(data):
    if isinstance(data, list):
        return data
    return [data]


def _print_table(data):
    rows = _as_rows(data)
    columns = ["id", "title", "year", "rating"]
    widths = {
        column: max(
            len(column),
            *[len(str(row.get(column, ""))) for row in rows if isinstance(row, dict)],
        )
        for column in columns
    }
    header = "  ".join(column.upper().ljust(widths[column]) for column in columns)
    print(header)
    print("  ".join("-" * widths[column] for column in columns))
    for row in rows:
        print(
            "  ".join(
                str(row.get(column, "") if row.get(column, "") is not None else "").ljust(
                    widths[column]
                )
                for column in columns
            )
        )


def _print_result(data, as_json):
    if as_json:
        print(to_json(data))
    else:
        _print_table(data)


def _search(args):
    service = _build_service(args)
    result = service.search(title=args.title, top=args.top)
    _print_result(result, args.json)


def _movie(args):
    service = _build_service(args)
    result = service.get_movie(id=args.id, images=args.images, trailer=args.trailer)
    _print_result(result, args.json)


def _top(args):
    service = _build_service(args)
    method = getattr(service, TOP_METHODS[args.kind])
    result = method(top=args.top)
    _print_result(result, args.json)


def build_parser():
    parser = argparse.ArgumentParser(prog="filmaffinity")
    parser.add_argument("--lang", default="es")
    parser.add_argument("--cache-backend", default="sqlite")

    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search")
    search.add_argument("title")
    search.add_argument("--top", type=int, default=10)
    search.add_argument("--json", action="store_true")
    search.set_defaults(func=_search)

    movie = subparsers.add_parser("movie")
    movie.add_argument("id")
    movie.add_argument("--images", action="store_true")
    movie.add_argument("--trailer", action="store_true")
    movie.add_argument("--json", action="store_true")
    movie.set_defaults(func=_movie)

    top = subparsers.add_parser("top")
    top.add_argument("--kind", choices=sorted(TOP_METHODS), default="filmaffinity")
    top.add_argument("--top", type=int, default=10)
    top.add_argument("--json", action="store_true")
    top.set_defaults(func=_top)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
