"""Focused tests for the isolated ECDC aggregate surveillance layer."""

from __future__ import annotations

import csv
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.ecdc_surveillance import (
    DATA_FIELDS,
    POPULATIONS,
    SOURCE_FIELDS,
    build_surveillance_records,
    load_surveillance_data,
    render_trend,
)


class EcdcSurveillanceTests(unittest.TestCase):
    def _write_source(self, path: Path, rows: list[dict[str, str]]) -> None:
        fields = [
            "HealthTopic",
            "Population",
            "Indicator",
            "Unit",
            "Time",
            "RegionCode",
            "RegionName",
            "NumValue",
            "TxtValue",
        ]
        with path.open("w", encoding="utf-8", newline="") as source_file:
            writer = csv.DictWriter(source_file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def _valid_rows(self) -> list[dict[str, str]]:
        return [
            {
                "HealthTopic": "Antimicrobial resistance",
                "Population": population,
                "Indicator": "R - resistant isolates, percentage  ",
                "Unit": "%",
                "Time": "2022",
                "RegionCode": "AT",
                "RegionName": "Austria",
                "NumValue": "12.345",
                "TxtValue": "",
            }
            for population in POPULATIONS
        ]

    def test_build_keeps_only_supported_numeric_single_class_rows(self):
        rows = self._valid_rows()
        rows.extend(
            [
                {
                    **rows[0],
                    "Population": (
                        "Escherichia coli|Combined resistance "
                        "(third-generation cephalosporin, fluoroquinolones and aminoglycoside)"
                    ),
                    "NumValue": "2.5",
                },
                {**rows[1], "Time": "2023", "NumValue": "-"},
            ]
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "exports.csv"
            self._write_source(source, rows)

            result = build_surveillance_records([source])

        self.assertEqual(len(result.records), 5)
        self.assertEqual(result.ignored_combined_rows, 1)
        self.assertEqual(result.ignored_unreported_rows, 1)
        self.assertTrue(all(record.resistant_pct == 12.35 for record in result.records))

    def test_build_rejects_missing_series_and_out_of_range_values(self):
        rows = self._valid_rows()[:-1]
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "exports.csv"
            self._write_source(source, rows)
            with self.assertRaisesRegex(ValueError, "Missing required ECDC"):
                build_surveillance_records([source])

            rows = self._valid_rows()
            rows[0]["NumValue"] = "100.1"
            self._write_source(source, rows)
            with self.assertRaisesRegex(ValueError, "between 0 and 100"):
                build_surveillance_records([source])

    def test_build_rejects_series_with_only_unreported_values(self):
        rows = self._valid_rows()
        rows[-1]["NumValue"] = "-"
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "exports.csv"
            self._write_source(source, rows)
            with self.assertRaisesRegex(ValueError, "No numeric observations"):
                build_surveillance_records([source])

    def test_bundled_snapshot_schema_values_and_series(self):
        records = load_surveillance_data()
        self.assertTrue(records)
        self.assertEqual(
            {(record.pathogen, record.antibiotic_group) for record in records},
            set(POPULATIONS.values()),
        )
        self.assertTrue(
            all(0 <= record.resistant_pct <= 100 for record in records)
        )

        series, status = render_trend(
            "E. coli — Fluoroquinolones", "Austria", records
        )
        self.assertTrue(series)
        self.assertEqual(series, sorted(series))
        self.assertIn("Austria", status)
        self.assertEqual(len(series[0]), 2)

    def test_bundled_snapshot_has_no_missing_or_duplicate_observations(self):
        records = load_surveillance_data()
        keys = {
            (
                record.country_code,
                record.pathogen,
                record.antibiotic_group,
                record.year,
            )
            for record in records
        }
        self.assertEqual(len(keys), len(records))
        self.assertTrue(all(record.country and record.country_code for record in records))

    def test_normalized_columns_match_published_contract(self):
        self.assertEqual(
            DATA_FIELDS,
            [
                "country_code",
                "country",
                "pathogen",
                "antibiotic_group",
                "year",
                "resistant_pct",
            ],
        )
        self.assertIn("NumValue", SOURCE_FIELDS)

    def test_invalid_source_and_bundled_schemas_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source.csv"
            source.write_text("Population\nEscherichia coli|Fluoroquinolones\n")
            with self.assertRaisesRegex(ValueError, "missing required columns"):
                build_surveillance_records([source])

            bundled = Path(temp_dir) / "bundled.csv"
            bundled.write_text("country,year\nAustria,2022\n")
            with self.assertRaisesRegex(ValueError, "expected columns in order"):
                load_surveillance_data(bundled)


if __name__ == "__main__":
    unittest.main()
