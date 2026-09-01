"""Command-line interface for the benchmark."""

from __future__ import annotations

import argparse
import json

from .metrics import compare_platforms, load_events


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse event-level conversational HRI logs")
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyse = subparsers.add_parser("analyse", help="compare two robot platforms")
    analyse.add_argument("events", help="CSV event log")
    analyse.add_argument("--platform-a", required=True)
    analyse.add_argument("--platform-b", required=True)
    args = parser.parse_args()
    result = compare_platforms(load_events(args.events), args.platform_a, args.platform_b)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
