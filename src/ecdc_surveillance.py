"""Read-only ECDC aggregate antimicrobial resistance surveillance data."""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "ecdc_surveillance.csv"

INDICATOR = "R - resistant isolates, percentage"
SOURCE_FIELDS = {
    "HealthTopic",
    "Population",
    "Indicator",
    "Unit",
    "Time",
    "RegionCode",
    "RegionName",
    "NumValue",
}
DATA_FIELDS = [
    "country_code",
    "country",
    "pathogen",
    "antibiotic_group",
    "year",
    "resistant_pct",
]

POPULATIONS = {
    "Escherichia coli|Fluoroquinolones": ("E. coli", "Fluoroquinolones"),
    "Escherichia coli|Third-generation cephalosporins": (
        "E. coli",
        "Third-generation cephalosporins",
    ),
    "Klebsiella pneumoniae|Carbapenems": (
        "K. pneumoniae",
        "Carbapenems",
    ),
    "Klebsiella pneumoniae|Third-generation cephalosporins": (
        "K. pneumoniae",
        "Third-generation cephalosporins",
    ),
    "Staphylococcus aureus|Meticillin (MRSA)": (
        "S. aureus",
        "Meticillin (MRSA)",
    ),
}

SERIES_LABELS = {
    "E. coli — Fluoroquinolones": ("E. coli", "Fluoroquinolones"),
    "E. coli — Third-generation cephalosporins": (
        "E. coli",
        "Third-generation cephalosporins",
    ),
    "K. pneumoniae — Carbapenems": ("K. pneumoniae", "Carbapenems"),
    "K. pneumoniae — Third-generation cephalosporins": (
        "K. pneumoniae",
        "Third-generation cephalosporins",
    ),
    "S. aureus (MRSA) — Meticillin": ("S. aureus", "Meticillin (MRSA)"),
}
ALLOWED_SERIES = set(POPULATIONS.values())


@dataclass(frozen=True)
class SurveillanceRecord:
    country_code: str
    country: str
    pathogen: str
    antibiotic_group: str
    year: int
    resistant_pct: float


@dataclass(frozen=True)
class BuildResult:
    records: list[SurveillanceRecord]
    ignored_combined_rows: int
    ignored_unreported_rows: int


def build_surveillance_records(source_paths: Iterable[str | Path]) -> BuildResult:
    """Normalize ECDC Atlas exports, retaining only the five single-class series."""
    records: dict[tuple[str, str, str, int], SurveillanceRecord] = {}
    found_populations: set[str] = set()
    ignored_combined = 0
    ignored_unreported = 0

    for source_path in source_paths:
        path = Path(source_path)
        with path.open("r", encoding="utf-8-sig", newline="") as source_file:
            reader = csv.DictReader(source_file)
            if reader.fieldnames is None:
                raise ValueError(f"{path}: CSV has no header")
            missing_fields = SOURCE_FIELDS - set(reader.fieldnames)
            if missing_fields:
                raise ValueError(
                    f"{path}: missing required columns: {', '.join(sorted(missing_fields))}"
                )

            for line_number, row in enumerate(reader, start=2):
                if (row.get("HealthTopic") or "").strip() != "Antimicrobial resistance":
                    raise ValueError(
                        f"{path}:{line_number}: unexpected health topic "
                        f"{row.get('HealthTopic')!r}"
                    )
                population = (row.get("Population") or "").strip()
                if "|Combined resistance" in population:
                    ignored_combined += 1
                    continue
                if population not in POPULATIONS:
                    raise ValueError(
                        f"{path}:{line_number}: unexpected population {population!r}"
                    )

                found_populations.add(population)
                indicator = (row.get("Indicator") or "").strip()
                if indicator != INDICATOR:
                    raise ValueError(
                        f"{path}:{line_number}: unexpected indicator {indicator!r}"
                    )
                if (row.get("Unit") or "").strip() != "%":
                    raise ValueError(f"{path}:{line_number}: expected percent unit")

                raw_value = (row.get("NumValue") or "").strip()
                if raw_value in {"", "-"}:
                    ignored_unreported += 1
                    continue
                try:
                    resistant_pct = float(raw_value)
                    year = int((row.get("Time") or "").strip())
                except ValueError as exc:
                    raise ValueError(
                        f"{path}:{line_number}: invalid year or percentage"
                    ) from exc

                if not math.isfinite(resistant_pct) or not 0 <= resistant_pct <= 100:
                    raise ValueError(
                        f"{path}:{line_number}: percentage must be between 0 and 100"
                    )
                if not 1900 <= year <= 2100:
                    raise ValueError(f"{path}:{line_number}: invalid year {year}")

                country_code = (row.get("RegionCode") or "").strip()
                country = (row.get("RegionName") or "").strip()
                if not country_code or not country:
                    raise ValueError(f"{path}:{line_number}: missing country")

                pathogen, antibiotic_group = POPULATIONS[population]
                record = SurveillanceRecord(
                    country_code=country_code,
                    country=country,
                    pathogen=pathogen,
                    antibiotic_group=antibiotic_group,
                    year=year,
                    resistant_pct=round(resistant_pct, 2),
                )
                key = (
                    record.country_code,
                    record.pathogen,
                    record.antibiotic_group,
                    record.year,
                )
                existing = records.get(key)
                if existing and existing != record:
                    raise ValueError(
                        f"{path}:{line_number}: conflicting duplicate observation {key}"
                    )
                records[key] = record

    missing_populations = set(POPULATIONS) - found_populations
    if missing_populations:
        raise ValueError(
            "Missing required ECDC population series: "
            + ", ".join(sorted(missing_populations))
        )
    present_series = {
        (record.pathogen, record.antibiotic_group) for record in records.values()
    }
    missing_series = ALLOWED_SERIES - present_series
    if missing_series:
        missing_labels = ", ".join(
            f"{pathogen} — {antibiotic_group}"
            for pathogen, antibiotic_group in sorted(missing_series)
        )
        raise ValueError(
            f"No numeric observations for required ECDC series: {missing_labels}"
        )

    ordered = sorted(
        records.values(),
        key=lambda item: (
            item.pathogen,
            item.antibiotic_group,
            item.country,
            item.year,
        ),
    )
    return BuildResult(ordered, ignored_combined, ignored_unreported)


def load_surveillance_data(
    path: str | Path = DATA_PATH,
) -> list[SurveillanceRecord]:
    """Load and validate the bundled, normalized ECDC snapshot."""
    data_path = Path(path)
    with data_path.open("r", encoding="utf-8-sig", newline="") as data_file:
        reader = csv.DictReader(data_file)
        if reader.fieldnames != DATA_FIELDS:
            raise ValueError(
                f"{data_path}: expected columns in order: {', '.join(DATA_FIELDS)}"
            )

        records: list[SurveillanceRecord] = []
        seen: set[tuple[str, str, str, int]] = set()
        for line_number, row in enumerate(reader, start=2):
            try:
                year = int(row["year"])
                resistant_pct = float(row["resistant_pct"])
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"{data_path}:{line_number}: invalid year or percentage"
                ) from exc
            if not math.isfinite(resistant_pct) or not 0 <= resistant_pct <= 100:
                raise ValueError(
                    f"{data_path}:{line_number}: percentage must be between 0 and 100"
                )
            if not 1900 <= year <= 2100:
                raise ValueError(f"{data_path}:{line_number}: invalid year {year}")
            if not all(
                (row["country_code"], row["country"], row["pathogen"], row["antibiotic_group"])
            ):
                raise ValueError(f"{data_path}:{line_number}: missing text field")

            record = SurveillanceRecord(
                country_code=row["country_code"],
                country=row["country"],
                pathogen=row["pathogen"],
                antibiotic_group=row["antibiotic_group"],
                year=year,
                resistant_pct=resistant_pct,
            )
            if (record.pathogen, record.antibiotic_group) not in ALLOWED_SERIES:
                raise ValueError(
                    f"{data_path}:{line_number}: unexpected surveillance series"
                )
            key = (
                record.country_code,
                record.pathogen,
                record.antibiotic_group,
                record.year,
            )
            if key in seen:
                raise ValueError(
                    f"{data_path}:{line_number}: duplicate observation {key}"
                )
            seen.add(key)
            records.append(record)

    if not records:
        raise ValueError(f"{data_path}: no surveillance observations")
    missing_series = ALLOWED_SERIES - {
        (record.pathogen, record.antibiotic_group) for record in records
    }
    if missing_series:
        raise ValueError(f"{data_path}: missing surveillance series {sorted(missing_series)}")
    return records


def country_choices(records: list[SurveillanceRecord]) -> list[str]:
    return sorted({record.country for record in records})


def render_trend(
    series_label: str,
    country: str,
    records: list[SurveillanceRecord],
) -> tuple[list[list[int | float]], str]:
    """Return a read-only annual table; this data is not used by the agent."""
    if series_label not in SERIES_LABELS:
        raise ValueError(f"Unknown ECDC surveillance series: {series_label}")
    pathogen, antibiotic_group = SERIES_LABELS[series_label]
    selected = sorted(
        (
            record
            for record in records
            if record.pathogen == pathogen
            and record.antibiotic_group == antibiotic_group
            and record.country == country
        ),
        key=lambda record: record.year,
    )
    rows = [[record.year, record.resistant_pct] for record in selected]
    if not rows:
        return [], f"No reported observations for {series_label} in {country}."
    return rows, f"{len(rows)} annual observations for {country}."
