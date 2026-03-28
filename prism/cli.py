"""Command-line entrypoints for the public PRISM repo."""

from __future__ import annotations

import argparse

from prism.publish import build_results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PRISM public repo CLI")
    parser.add_argument("command", choices=["results"], help="Command to execute")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "results":
        outputs = build_results()
        for key, path in outputs.items():
            print(f"{key}: {path}")


if __name__ == "__main__":
    main()

