"""CLI for MXO4 SCPI catalog and recipes."""

from __future__ import annotations

import argparse
import json
import sys

from mxo4_sigcapture.scpi import ScpiCatalog


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MXO4 SCPI catalog")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("count")
    sub.add_parser("connection", help="Show VISA / socket connection strings")

    p_find = sub.add_parser("find")
    p_find.add_argument("pattern")

    p_show = sub.add_parser("show")
    p_show.add_argument("name")

    p_recipe = sub.add_parser("recipe")
    p_recipe.add_argument("name")
    p_recipe.add_argument("-n", type=int, default=1, help="channel placeholder {n}")

    args = parser.parse_args(argv)
    cat = ScpiCatalog.load()

    if args.cmd == "count":
        print(len(cat))
    elif args.cmd == "connection":
        print(json.dumps(cat.connection, indent=2))
    elif args.cmd == "find":
        for cmd in cat.search(args.pattern):
            print(f"{cmd.name}\tp{cmd.page}\t{cmd.summary[:60]}")
    elif args.cmd == "show":
        print(cat.help_text(args.name))
    elif args.cmd == "recipe":
        steps = cat.recipe_steps(args.name, n=args.n)
        for step in steps:
            print(step)
    return 0


if __name__ == "__main__":
    sys.exit(main())
