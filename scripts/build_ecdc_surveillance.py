#!/usr/bin/env python3
"""Build the bundled ECDC aggregate surveillance snapshot from Atlas CSV exports."""

from __future__ import annotations

import argparse
import csv
import os
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.ecdc_surveillance import DATA_FIELDS, build_surveillance_records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="ECDC Surveillance Atlas CSV exports")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "ecdc_surveillance.csv",
    )
    args = parser.parse_args(argv)

    result = build_surveillance_records(args.inputs)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(
            output_file,
            fieldnames=DATA_FIELDS,
            lineterminator="\n",
        )
        writer.writeheader()
        for record in result.records:
            writer.writerow(asdict(record))

    print(f"Wrote {len(result.records)} observations to {args.out}")
    print(
        f"Ignored {result.ignored_combined_rows} combined-resistance rows and "
        f"{result.ignored_unreported_rows} unreported rows."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
