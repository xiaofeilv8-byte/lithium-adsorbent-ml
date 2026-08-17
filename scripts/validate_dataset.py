#!/usr/bin/env python3
"""Validate lithium-adsorbent structure–performance CSV files.

Usage:
    python scripts/validate_dataset.py path/to/dataset.csv
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

REQUIRED_COLUMNS = [
    "record_id",
    "paper_id",
    "material_name",
    "material_family",
    "Li_adsorption_capacity_qe",
    "possible_ML_task",
    "suggested_target_property",
    "feature_completeness_level",
    "data_quality_level",
    "extraction_source",
]

BOOLEAN_COLUMNS = [
    "Ti_based_or_not",
    "Mn_based_or_not",
    "Al_based_or_not",
    "LDH_or_not",
    "acid_treatment_or_not",
    "H_exchange_or_not",
    "organic_material_or_not",
    "ion_imprinted_or_not",
    "boron_present_or_not",
    "sulfate_present_or_not",
    "carbonate_present_or_not",
    "silica_present_or_not",
]

NUMERIC_COLUMNS = [
    "year",
    "particle_size",
    "calcination_temperature",
    "interlayer_spacing",
    "lattice_parameter",
    "synthesis_pH",
    "synthesis_temperature",
    "synthesis_time",
    "hydrothermal_temperature",
    "hydrothermal_time",
    "aging_time",
    "drying_temperature",
    "BET_surface_area",
    "pore_volume",
    "average_pore_size",
    "zeta_potential",
    "pHpzc",
    "functional_group_density",
    "ion_exchange_capacity",
    "surface_OH_density",
    "water_contact_angle",
    "Li_initial_concentration",
    "adsorbent_dosage",
    "solution_pH",
    "temperature",
    "contact_time",
    "liquid_solid_ratio",
    "ionic_strength",
    "Mg_Li_ratio",
    "Na_Li_ratio",
    "K_Li_ratio",
    "Ca_Li_ratio",
    "Li_adsorption_capacity_qe",
    "Li_maximum_capacity_Qmax",
    "Li_removal_efficiency",
    "distribution_coefficient_Kd",
    "Li_Mg_separation_factor",
    "Li_Na_separation_factor",
    "Li_K_separation_factor",
    "Li_Ca_separation_factor",
    "selectivity_coefficient",
    "equilibrium_time",
    "cycle_number",
    "capacity_retention",
    "dissolution_loss",
]

MISSING_TOKENS = {"", "missing", "na", "n/a", "nan", "none", "null"}
BOOLEAN_ALLOWED = {"yes", "no", "true", "false", "0", "1"} | MISSING_TOKENS


def is_missing(value: str) -> bool:
    return value.strip().lower() in MISSING_TOKENS


def is_number(value: str) -> bool:
    if is_missing(value):
        return True
    try:
        number = float(value)
        return math.isfinite(number)
    except ValueError:
        return False


def validate(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not path.exists():
        return [f"File not found: {path}"], warnings

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []

        if not header:
            return ["CSV has no header."], warnings

        duplicates = sorted({name for name in header if header.count(name) > 1})
        if duplicates:
            errors.append("Duplicate columns: " + ", ".join(duplicates))

        missing_required = [c for c in REQUIRED_COLUMNS if c not in header]
        if missing_required:
            errors.append("Missing required columns: " + ", ".join(missing_required))

        rows = list(reader)

    if not rows:
        warnings.append("Dataset contains a header but no data rows.")
        return errors, warnings

    seen_ids: set[str] = set()
    usable_rows = 0

    for index, row in enumerate(rows, start=2):
        record_id = (row.get("record_id") or "").strip()

        if record_id and not is_missing(record_id):
            if record_id in seen_ids:
                errors.append(f"Row {index}: duplicate record_id '{record_id}'.")
            seen_ids.add(record_id)
        else:
            warnings.append(f"Row {index}: record_id is missing.")

        for column in BOOLEAN_COLUMNS:
            if column in row:
                value = (row.get(column) or "").strip().lower()
                if value not in BOOLEAN_ALLOWED:
                    warnings.append(
                        f"Row {index}: {column}='{row.get(column)}' is not a standard boolean value."
                    )

        for column in NUMERIC_COLUMNS:
            if column in row:
                value = row.get(column) or ""
                if not is_number(value):
                    warnings.append(
                        f"Row {index}: {column}='{value}' is not numeric or a recognized missing value."
                    )

        key_values = [
            row.get("material_name", ""),
            row.get("material_family", ""),
            row.get("Li_adsorption_capacity_qe", ""),
        ]
        if any(not is_missing(v or "") for v in key_values):
            usable_rows += 1

    if usable_rows == 0:
        warnings.append(
            "No row contains usable material/performance values. "
            "This is acceptable for the distributed blank/example template, "
            "but not for a training dataset."
        )

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate lithium-adsorbent structure–performance CSV files."
    )
    parser.add_argument("csv_path", type=Path, help="CSV file to validate")
    args = parser.parse_args()

    errors, warnings = validate(args.csv_path)

    print(f"Validated: {args.csv_path}")

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")

    if errors:
        print(f"Result: FAIL ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1

    print(f"Result: PASS ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
