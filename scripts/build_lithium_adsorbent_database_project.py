from __future__ import annotations

import csv
import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

import pandas as pd


TARGET = Path(r"E:\Research\ML-adsorbent-review")
SOURCE = Path(r"E:\Research\ML-adsorbent-review")
SOURCE_MATRIX = SOURCE / "literature" / "literature_matrix_working.csv"


LIT_COLUMNS = [
    "paper_id", "title", "year", "journal", "DOI", "material_family",
    "material_subfamily", "material_name", "lithium_recovery_related",
    "whether_LDH_related", "whether_titanium_based", "whether_manganese_based",
    "whether_aluminum_based", "organic_material_or_not", "ion_imprinted_or_not",
    "MOF_COF_or_not", "membrane_or_electrochemical_or_not", "application_area",
    "adsorption_target", "solution_system", "real_brine_or_synthetic_solution",
    "brine_type", "competing_ions", "ML_related_or_not", "ML_task",
    "ML_model", "input_features", "output_property", "descriptor_type",
    "dataset_size", "validation_method", "performance_metrics",
    "interpretability_method", "DFT_or_MD_combined_or_not", "key_findings",
    "limitations", "suitability_for_structure_performance_database",
    "suitability_for_ML_modeling", "priority_for_full_text_extraction",
    "notes", "information_source",
]

FAMILIES = [
    "LDH-based adsorbents",
    "Ti-based lithium adsorbents",
    "Mn-based lithium ion sieves",
    "Al-based lithium adsorbents",
    "ion-imprinted polymers / membranes",
    "crown ether / calixarene / macrocyclic ligand materials",
    "MOF / COF / porous organic materials",
    "hybrid/composite adsorbents",
    "electrochemical / membrane lithium-selective materials",
    "non-lithium but ML-method transferable papers",
    "uncertain",
]

SP_COLUMNS = [
    "record_id", "paper_id", "title", "year", "journal", "DOI",
    "material_name", "material_family", "material_subfamily", "active_phase",
    "support_or_matrix", "composite_component", "morphology", "particle_size",
    "granulated_or_powder", "membrane_or_bead_or_powder", "Ti_based_or_not",
    "Mn_based_or_not", "Al_based_or_not", "LDH_or_not", "crystal_structure",
    "precursor_phase", "acid_treatment_or_not", "H_exchange_or_not",
    "Li_extraction_method", "calcination_temperature", "interlayer_spacing",
    "lattice_parameter", "crystallinity_indicator", "organic_material_or_not",
    "ion_imprinted_or_not", "template_ion", "functional_monomer", "crosslinker",
    "ligand_or_binding_group", "polymer_matrix", "porogen_or_solvent",
    "imprinting_factor", "crown_ether_or_macrocycle_type", "functional_group_type",
    "synthesis_method", "synthesis_pH", "synthesis_temperature", "synthesis_time",
    "hydrothermal_temperature", "hydrothermal_time", "aging_time",
    "drying_temperature", "activation_method", "BET_surface_area", "pore_volume",
    "average_pore_size", "zeta_potential", "pHpzc", "functional_group_density",
    "ion_exchange_capacity", "surface_OH_density", "water_contact_angle",
    "mechanical_stability_indicator", "Li_initial_concentration",
    "adsorbent_dosage", "solution_pH", "temperature", "contact_time",
    "liquid_solid_ratio", "ionic_strength", "real_brine_or_synthetic_solution",
    "brine_type", "Mg_Li_ratio", "Na_Li_ratio", "K_Li_ratio", "Ca_Li_ratio",
    "coexisting_ions", "boron_present_or_not", "sulfate_present_or_not",
    "carbonate_present_or_not", "silica_present_or_not", "Li_adsorption_capacity_qe",
    "Li_maximum_capacity_Qmax", "Li_removal_efficiency", "distribution_coefficient_Kd",
    "Li_Mg_separation_factor", "Li_Na_separation_factor", "Li_K_separation_factor",
    "Li_Ca_separation_factor", "selectivity_coefficient", "equilibrium_time",
    "kinetic_model", "isotherm_model", "regeneration_method", "desorption_agent",
    "cycle_number", "capacity_retention", "dissolution_loss",
    "structural_stability_after_cycles", "possible_ML_task",
    "suggested_target_property", "feature_completeness_level", "data_quality_level",
    "extraction_source", "notes",
]


def make_dirs() -> None:
    for rel in [
        "data/raw", "data/translated", "data/processed",
        "data/lithium_adsorbent_database", "data/ml_dataset_template", "data/notes",
        "scripts", "notebooks", "outputs", "outputs/ml_results", "prompts", "manuscript",
    ]:
        (TARGET / rel).mkdir(parents=True, exist_ok=True)


def contains(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.I) for pattern in patterns)


def text_blob(row: pd.Series) -> str:
    cols = [
        "Title", "Abstract", "Author keywords", "Keywords Plus",
        "Preliminary topic tags", "Source export file", "Search topic",
        "Application domain", "Adsorbent/material class", "ML task type",
        "Suggested manuscript section", "Use in review",
    ]
    return " ".join(str(row.get(col, "")) for col in cols).lower()


def evidence_blob(row: pd.Series) -> str:
    cols = ["Title", "Abstract", "Author keywords", "Keywords Plus", "Source export file", "Search topic"]
    return " ".join(str(row.get(col, "")) for col in cols).lower()


def classify(row: pd.Series) -> dict[str, str | bool]:
    text = text_blob(row)
    ev = evidence_blob(row)
    lithium = contains(ev, [
        r"\blithium\b", r"\bli\+\b", r"\bli-ion\b", r"\bli/al\b", r"\blial\b",
        r"lithium_adsorption", r"lithium_adsorbent", r"lithium extraction",
        r"lithium recovery", r"salt lake brine", r"\bbrine\b",
    ])
    ml = contains(text, [r"machine learning", r"artificial intelligence", r"\bml\b", r"data-driven", r"deep learning", r"xgboost", r"random forest", r"shap", r"neural network", r"bayesian optimization", r"active learning"])
    adsorption = contains(text, [r"adsorp", r"extraction", r"recovery", r"capture", r"removal", r"separation", r"selectiv"])
    ldh = contains(text, [r"layered double hydroxide", r"\bldh\b", r"layered hydroxide", r"lithium-aluminum layered", r"li/al-ldh", r"lial"])
    ti = contains(text, [r"titanium", r"titanate", r"h2tio3", r"h4ti5o12", r"li4ti5o12", r"ti-based"])
    mn = contains(text, [r"manganese", r"mn-based", r"limn", r"lithium manganese oxide", r"spinel"])
    al = contains(text, [r"aluminum", r"aluminium", r"\bal-?based", r"li/al", r"lial", r"al-ldh"])
    ion_imp = contains(text, [r"ion-imprinted", r"ion imprinted", r"imprinted polymer", r"imprinted membrane", r"\biip\b"])
    organic = contains(text, [r"polymer", r"organic ligand", r"crown ether", r"calixarene", r"cryptand", r"macrocyclic", r"porous organic polymer", r"covalent organic polymer"])
    macro = contains(text, [r"crown ether", r"calixarene", r"cryptand", r"macrocyclic"])
    mofcof = contains(text, [r"\bmof\b", r"metal-organic framework", r"\bcof\b", r"covalent organic framework"])
    membrane_echem = contains(text, [r"membrane", r"electrochemical", r"capacitive deionization", r"intercalation/deintercalation"])
    composite = contains(text, [r"composite", r"hybrid", r"supported", r"magnetic", r"biochar", r"carbon-supported", r"graphene"])
    methodology_only = ml and not any([lithium, ldh, ti, mn, al, ion_imp, organic, mofcof])

    if ldh:
        fam = "LDH-based adsorbents"
        sub = "Li/Al-LDH or other LDH-derived adsorbent" if lithium or al else "other LDH-derived adsorbent"
    elif ti and lithium:
        fam, sub = "Ti-based lithium adsorbents", "titanate / titanium lithium ion sieve"
    elif mn and lithium:
        fam, sub = "Mn-based lithium ion sieves", "lithium manganese oxide / Mn ion sieve"
    elif al and lithium:
        fam, sub = "Al-based lithium adsorbents", "aluminum-based lithium adsorbent"
    elif ion_imp:
        fam, sub = "ion-imprinted polymers / membranes", "lithium ion-imprinted material" if lithium else "ion-imprinted material"
    elif macro:
        fam, sub = "crown ether / calixarene / macrocyclic ligand materials", "macrocyclic ligand-based adsorbent"
    elif mofcof:
        fam, sub = "MOF / COF / porous organic materials", "MOF/COF/porous framework"
    elif membrane_echem and lithium:
        fam, sub = "electrochemical / membrane lithium-selective materials", "membrane or electrochemical lithium-selective material"
    elif composite and lithium:
        fam, sub = "hybrid/composite adsorbents", "composite/hybrid lithium adsorbent"
    elif methodology_only:
        fam, sub = "non-lithium but ML-method transferable papers", "methodology-only"
    else:
        fam, sub = "uncertain", "uncertain"

    target_terms = []
    if lithium:
        target_terms.append("Li+")
    if contains(text, [r"phosphate"]):
        target_terms.append("phosphate")
    if contains(text, [r"uranium|uranyl"]):
        target_terms.append("uranium/uranyl")
    if contains(text, [r"chromium|cr\(vi\)"]):
        target_terms.append("Cr(VI)")
    competing = []
    for ion, pattern in [
        ("Mg2+", r"mg|magnesium"), ("Na+", r"na\+|sodium"),
        ("K+", r"k\+|potassium"), ("Ca2+", r"ca\+|calcium"),
        ("SO4(2-)", r"sulfate"), ("boron/borate", r"boron|borate"),
    ]:
        if contains(text, [pattern]):
            competing.append(ion)

    ml_task = "missing"
    if ml and contains(text, [r"prediction|predicting|predict"]):
        ml_task = "performance prediction"
    elif ml and contains(text, [r"optimization|optimized|screening|design"]):
        ml_task = "screening/optimization/design"
    elif ml:
        ml_task = "ML-related, task unclear from metadata"

    models = []
    for name, pattern in [
        ("random forest", r"random forest"), ("XGBoost", r"xgboost"),
        ("ANN/neural network", r"artificial neural network|\bann\b|neural network"),
        ("Gaussian process", r"gaussian process"),
        ("SVR/SVM", r"support vector|\bsvr\b|\bsvm\b"),
        ("deep learning", r"deep learning"),
    ]:
        if contains(text, [pattern]):
            models.append(name)

    suit_db = "high" if lithium and adsorption and fam not in ["non-lithium but ML-method transferable papers", "uncertain"] else (
        "medium" if any([lithium, ldh, ti, mn, al, ion_imp, mofcof]) else ("low" if methodology_only else "uncertain")
    )
    suit_ml = "high" if ml and any([lithium, ldh, ti, mn, al, ion_imp]) else ("medium" if ml or suit_db in ["high", "medium"] else "low")
    priority = "high" if suit_db == "high" or (ml and lithium) else ("medium" if suit_db == "medium" or ml else "low")

    return {
        "lithium": lithium, "ml": ml, "adsorption": adsorption, "ldh": ldh, "ti": ti,
        "mn": mn, "al": al, "ion_imp": ion_imp, "organic": organic, "mofcof": mofcof,
        "membrane_echem": membrane_echem, "methodology_only": methodology_only,
        "fam": fam, "sub": sub,
        "application": "lithium recovery" if lithium else ("ML methodology transfer" if methodology_only else "adsorption/materials background"),
        "solution": "brine/salt lake/unconventional water" if contains(text, [r"brine", r"salt lake", r"unconventional water"]) else "missing",
        "brine_type": "salt lake brine" if contains(text, [r"salt lake"]) else ("brine" if contains(text, [r"brine"]) else "missing"),
        "target": "; ".join(target_terms) if target_terms else "missing",
        "competing": "; ".join(competing) if competing else "missing",
        "ml_task": ml_task,
        "models": "; ".join(models) if models else "missing",
        "input_features": "mentioned in metadata" if contains(text, [r"descriptor|feature|structure|condition|composition"]) else "missing",
        "output_property": "adsorption/recovery performance" if adsorption else "missing",
        "interp": "feature importance / SHAP mentioned" if contains(text, [r"shap|feature importance|interpretable|explainable"]) else "missing",
        "dftmd": "yes" if contains(text, [r"\bdft\b|density functional|molecular dynamics|\bmd\b"]) else "missing",
        "suit_db": suit_db, "suit_ml": suit_ml, "priority": priority,
    }


def build_literature_matrix() -> pd.DataFrame:
    if not SOURCE_MATRIX.exists():
        return pd.DataFrame(columns=LIT_COLUMNS)
    source_df = pd.read_csv(SOURCE_MATRIX, dtype=str, encoding="utf-8-sig").fillna("")
    rows: list[dict[str, str]] = []
    for _, row in source_df.iterrows():
        c = classify(row)
        if not any([c["lithium"], c["ldh"], c["ti"], c["mn"], c["al"], c["ion_imp"], c["mofcof"], c["methodology_only"]]):
            continue
        rows.append({
            "paper_id": row.get("Paper ID", "missing") or "missing",
            "title": row.get("Title", "missing") or "missing",
            "year": row.get("Year", "missing") or "missing",
            "journal": row.get("Journal", "missing") or "missing",
            "DOI": row.get("DOI", "missing") or "missing",
            "material_family": c["fam"], "material_subfamily": c["sub"],
            "material_name": "missing",
            "lithium_recovery_related": "yes" if c["lithium"] else "no",
            "whether_LDH_related": "yes" if c["ldh"] else "no",
            "whether_titanium_based": "yes" if c["ti"] else "no",
            "whether_manganese_based": "yes" if c["mn"] else "no",
            "whether_aluminum_based": "yes" if c["al"] else "no",
            "organic_material_or_not": "yes" if c["organic"] else "no",
            "ion_imprinted_or_not": "yes" if c["ion_imp"] else "no",
            "MOF_COF_or_not": "yes" if c["mofcof"] else "no",
            "membrane_or_electrochemical_or_not": "yes" if c["membrane_echem"] else "no",
            "application_area": c["application"],
            "adsorption_target": c["target"],
            "solution_system": c["solution"],
            "real_brine_or_synthetic_solution": "uncertain" if c["solution"] != "missing" else "missing",
            "brine_type": c["brine_type"],
            "competing_ions": c["competing"],
            "ML_related_or_not": "yes" if c["ml"] else "no",
            "ML_task": c["ml_task"], "ML_model": c["models"],
            "input_features": c["input_features"],
            "output_property": c["output_property"],
            "descriptor_type": "material + solution + operation descriptors possible" if any([c["lithium"], c["ldh"], c["ml"]]) else "missing",
            "dataset_size": "missing", "validation_method": "missing", "performance_metrics": "missing",
            "interpretability_method": c["interp"],
            "DFT_or_MD_combined_or_not": c["dftmd"],
            "key_findings": "missing", "limitations": "missing",
            "suitability_for_structure_performance_database": c["suit_db"],
            "suitability_for_ML_modeling": c["suit_ml"],
            "priority_for_full_text_extraction": c["priority"],
            "notes": "methodology-only" if c["methodology_only"] else "classification based on title/abstract/keywords only; full text required",
            "information_source": "existing literature_matrix_working.csv metadata; specified docx abstracts not found",
        })
    return pd.DataFrame(rows, columns=LIT_COLUMNS)


def write_csv_and_xlsx(df: pd.DataFrame) -> None:
    out_csv = TARGET / "data/processed/literature_matrix_lithium_adsorbents.csv"
    out_xlsx = TARGET / "data/processed/literature_matrix_lithium_adsorbents.xlsx"
    df.to_csv(out_csv, index=False, encoding="utf-8-sig")
    try:
        df.to_excel(out_xlsx, index=False)
    except Exception as exc:
        write_simple_xlsx(df, out_xlsx)
        (TARGET / "data/processed/literature_matrix_lithium_adsorbents_xlsx_error.txt").write_text(
            f"pandas Excel writer unavailable ({exc}); generated basic OpenXML XLSX fallback.",
            encoding="utf-8",
        )


def excel_col(n: int) -> str:
    s = ""
    n += 1
    while n:
        n, rem = divmod(n - 1, 26)
        s = chr(65 + rem) + s
    return s


def write_simple_xlsx(df: pd.DataFrame, path: Path) -> None:
    """Write a minimal Excel workbook with inline strings and one worksheet."""
    rows = [list(df.columns)] + df.astype(str).values.tolist()
    sheet_rows = []
    for r_idx, row in enumerate(rows, start=1):
        cells = []
        for c_idx, value in enumerate(row):
            ref = f"{excel_col(c_idx)}{r_idx}"
            value = "" if value == "nan" else value
            cells.append(f'<c r="{ref}" t="inlineStr"><is><t>{escape(value)}</t></is></c>')
        sheet_rows.append(f'<row r="{r_idx}">{"".join(cells)}</row>')
    dimension = f"A1:{excel_col(len(rows[0]) - 1)}{len(rows)}" if rows else "A1"
    sheet_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<dimension ref="{dimension}"/>
<sheetViews><sheetView workbookViewId="0"/></sheetViews>
<sheetFormatPr defaultRowHeight="15"/>
<sheetData>{"".join(sheet_rows)}</sheetData>
</worksheet>'''
    workbook_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="literature_matrix" sheetId="1" r:id="rId1"/></sheets></workbook>'''
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''
    wb_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>'''
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>'''
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", workbook_xml)
        z.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        z.writestr("xl/worksheets/sheet1.xml", sheet_xml)


def write_classification(df: pd.DataFrame) -> None:
    rows = []
    for fam in FAMILIES:
        sub = df[df["material_family"] == fam]
        rows.append({
            "material_family": fam,
            "record_count": len(sub),
            "with_capacity_or_selectivity_data_in_metadata": int(sub["output_property"].str.contains("adsorption|recovery|selectivity", case=False, na=False).sum()) if not sub.empty else 0,
            "review_only_or_methodology_count": int(((sub["notes"].str.contains("methodology-only", na=False)) | (sub["suitability_for_structure_performance_database"].isin(["low", "uncertain"]))).sum()) if not sub.empty else 0,
            "suitable_for_structure_performance_database_high_or_medium": int(sub["suitability_for_structure_performance_database"].isin(["high", "medium"]).sum()) if not sub.empty else 0,
            "priority_full_text_high": int((sub["priority_for_full_text_extraction"] == "high").sum()) if not sub.empty else 0,
            "notes": "counts based on metadata classification only",
        })
    pd.DataFrame(rows).to_csv(TARGET / "data/processed/material_family_classification.csv", index=False, encoding="utf-8-sig")


def write_database_templates() -> None:
    template = TARGET / "data/lithium_adsorbent_database/lithium_adsorbent_structure_performance_template.csv"
    with template.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(SP_COLUMNS)
        writer.writerow(["example_missing_do_not_train"] + ["missing"] * (len(SP_COLUMNS) - 1))

    numeric = {
        "particle_size", "calcination_temperature", "interlayer_spacing", "lattice_parameter",
        "synthesis_pH", "synthesis_temperature", "synthesis_time", "hydrothermal_temperature",
        "hydrothermal_time", "aging_time", "drying_temperature", "BET_surface_area",
        "pore_volume", "average_pore_size", "zeta_potential", "pHpzc",
        "functional_group_density", "ion_exchange_capacity", "surface_OH_density",
        "water_contact_angle", "Li_initial_concentration", "adsorbent_dosage",
        "solution_pH", "temperature", "contact_time", "liquid_solid_ratio", "ionic_strength",
        "Mg_Li_ratio", "Na_Li_ratio", "K_Li_ratio", "Ca_Li_ratio",
        "Li_adsorption_capacity_qe", "Li_maximum_capacity_Qmax", "Li_removal_efficiency",
        "distribution_coefficient_Kd", "Li_Mg_separation_factor", "Li_Na_separation_factor",
        "Li_K_separation_factor", "Li_Ca_separation_factor", "selectivity_coefficient",
        "equilibrium_time", "cycle_number", "capacity_retention", "dissolution_loss",
    }
    outputs = {
        "Li_adsorption_capacity_qe", "Li_maximum_capacity_Qmax", "Li_removal_efficiency",
        "distribution_coefficient_Kd", "Li_Mg_separation_factor", "Li_Na_separation_factor",
        "Li_K_separation_factor", "Li_Ca_separation_factor", "selectivity_coefficient",
        "equilibrium_time", "capacity_retention", "dissolution_loss",
        "structural_stability_after_cycles",
    }
    units = {
        "BET_surface_area": "m2/g", "pore_volume": "cm3/g", "average_pore_size": "nm",
        "zeta_potential": "mV", "calcination_temperature": "deg C",
        "interlayer_spacing": "nm or Angstrom", "Li_initial_concentration": "mg/L or mmol/L",
        "adsorbent_dosage": "g/L or g", "contact_time": "min or h",
        "Li_adsorption_capacity_qe": "mg/g or mmol/g",
        "Li_maximum_capacity_Qmax": "mg/g or mmol/g",
        "Li_removal_efficiency": "%", "distribution_coefficient_Kd": "mL/g",
    }
    lines = [
        "# Lithium Adsorbent Descriptor Dictionary\n",
        "Each field must be extracted from full text, tables, figures, or SI. If unavailable, write `missing`; do not infer numeric values from abstracts.\n",
        "| Field | Meaning | Suggested unit | Type | ML role | Notes |",
        "|---|---|---|---|---|---|",
    ]
    for col in SP_COLUMNS:
        field_type = "numeric" if col in numeric else "categorical/text"
        role = "output target" if col in outputs else ("metadata" if col in {"record_id", "paper_id", "title", "year", "journal", "DOI", "notes", "extraction_source"} else "input feature")
        lines.append(f"| `{col}` | {col.replace('_', ' ')} | {units.get(col, 'as reported / not applicable')} | {field_type} | {role} | Use `missing` when not explicitly available. |")
    (TARGET / "data/lithium_adsorbent_database/lithium_adsorbent_descriptor_dictionary.md").write_text("\n".join(lines), encoding="utf-8")

    (TARGET / "data/lithium_adsorbent_database/data_extraction_guidelines.md").write_text("""# Data Extraction Guidelines for Lithium Adsorbent Structure-Performance Database

Each row in `lithium_adsorbent_structure_performance_template.csv` should represent one explicit material-condition-performance data point, not one paper.

## Source Priority
1. Main-text tables.
2. Supplementary information tables.
3. Explicit values in text.
4. Digitized values from figures using WebPlotDigitizer or careful manual extraction.
5. Abstract metadata only for bibliographic screening, not final numeric ML data.

## Do Not Invent Values
Do not infer adsorption capacity, selectivity, BET surface area, pH, temperature, dosage, or model metrics from abstracts. If a value is absent, write `missing` or `not available`.

## Figure Data
Data in plots must be extracted later using WebPlotDigitizer or manually checked against the original figure axis. Mark such rows as `digitized_from_figure` in `extraction_source`.

## Units and Quality
Record the unit as reported when unit harmonization is not yet complete. Use `feature_completeness_level` and `data_quality_level` to mark whether material descriptors, solution descriptors, and performance labels are sufficiently complete for ML.
""", encoding="utf-8")

    (TARGET / "data/lithium_adsorbent_database/reverse_design_descriptor_framework.md").write_text("""# Reverse Design Descriptor Framework for Lithium Adsorbents

## Purpose
This framework supports future ML analysis and inverse design of lithium recovery adsorbents. It is broader than the previous LDH-only review scope and includes Ti-based ion sieves, Mn-based ion sieves, LDH/aluminum-based adsorbents, ion-imprinted materials, organic ligand materials, MOF/COF systems, and composites.

## Material Descriptors
- material_family
- active phase
- metal composition
- Li vacancy / H exchange
- interlayer structure
- functional groups
- ligand type
- pore structure
- surface charge
- hydrophilicity
- stability indicators

## Solution-Environment Descriptors
- Li concentration
- Mg/Li ratio
- pH
- competing ions
- ionic strength
- brine type
- temperature

## Performance Targets
- Li capacity
- Li/Mg selectivity
- regeneration stability
- dissolution loss
- cycle retention

## Reverse Design Logic
1. Predict performance from material and solution descriptors.
2. Use feature importance / SHAP only after model validation to identify influential factors.
3. Screen combinations that may balance high capacity, high selectivity, and high stability.
4. Return to experimental design for synthesis feasibility and validation.

## Value for Ti-Based Lithium Adsorbent Research
- Enables comparison of Ti-based adsorbents with LDH, ion-imprinted polymers, Mn-based ion sieves, and organic ligand adsorbents.
- Provides data-driven reference for Ti-based modification directions, such as crystal phase, H/Li exchange, morphology, and dissolution/stability control.
- Supports doctoral work extending from literature review toward data-driven materials design.
""", encoding="utf-8")


def write_notes_and_outputs(df: pd.DataFrame, docx_found: list[Path]) -> None:
    counts = df["material_family"].value_counts().to_dict() if not df.empty else {}
    high_medium = df[df["suitability_for_structure_performance_database"].isin(["high", "medium"])] if not df.empty else pd.DataFrame()
    priority = df[df["priority_for_full_text_extraction"] == "high"].head(30) if not df.empty else pd.DataFrame()

    summary = ["# Lithium Adsorbent Literature Summary\n\n", "## Source Status\n\n"]
    if docx_found:
        summary.append(f"- Found {len(docx_found)} docx files:\n")
        for p in docx_found:
            summary.append(f"  - `{p}`\n")
    else:
        summary.append("- No expected docx abstract files were found. The current matrix was generated from `literature_matrix_working.csv` metadata.\n")
    summary.append("\n## Material Family Counts\n\n")
    for fam in FAMILIES:
        summary.append(f"- {fam}: {counts.get(fam, 0)}\n")
    summary.append(f"\n## Suitable for Structure-Performance Database\n\n- High/medium suitability: {len(high_medium)}\n")
    summary.append("\n## Priority Full-Text Reading Candidates\n\n")
    for _, r in priority.iterrows():
        summary.append(f"- {r['paper_id']}: {r['title']} ({r['material_family']})\n")
    summary.append("\n## Notes\n\n- Counts are metadata-based and require full-text verification.\n- Numeric performance values were not extracted from abstracts.\n")
    (TARGET / "data/notes/lithium_adsorbent_literature_summary.md").write_text("".join(summary), encoding="utf-8")

    (TARGET / "data/notes/literature_gap_and_search_keywords_lithium_adsorbents.md").write_text("""# Literature Gaps and Search Keywords for Lithium Adsorbent Database

## Priority Literature Types To Add
1. Ti-based lithium adsorbents.
2. Ion-imprinted polymers and membranes.
3. Mn-based ion sieves.
4. Li/Al-LDH and aluminum-based adsorbents.
5. Organic ligand / macrocycle adsorbents.
6. MOF/COF lithium-selective materials.

## Search Keywords
- lithium adsorbent structure performance database
- lithium recovery adsorbent machine learning
- machine learning lithium extraction materials
- titanium lithium ion sieve adsorbent
- titanate lithium adsorbent brine
- H2TiO3 lithium adsorbent
- H4Ti5O12 lithium adsorbent
- manganese lithium ion sieve adsorbent
- lithium aluminum layered double hydroxide adsorbent
- Li Al LDH lithium adsorption brine
- lithium ion-imprinted polymer adsorbent
- Li+ ion imprinted polymer lithium recovery
- lithium imprinted membrane
- lithium selective crown ether adsorbent
- lithium selective calixarene adsorbent
- lithium selective porous organic polymer
- lithium adsorption organic ligand material
- MOF lithium recovery adsorbent
- COF lithium recovery adsorbent
- lithium adsorbent selectivity Mg Li
- lithium recovery salt lake brine adsorbent
""", encoding="utf-8")

    (TARGET / "outputs/ML_feasibility_assessment_lithium_adsorbents.md").write_text("""# ML Feasibility Assessment for Lithium Adsorbents

## What Can Be Done From Abstracts/Metadata Now
- Build a bibliographic and screening matrix.
- Classify papers by material family and ML relevance.
- Identify likely high-priority full-text extraction targets.
- Design descriptor fields and database structure.

## What Requires Full-Text Reading
- Adsorption capacity, selectivity, Kd, separation factors, BET, pore volume, pH, dosage, temperature, cycle retention, dissolution loss, and exact brine composition.
- Dataset size, validation method, model metrics, and feature importance values.
- Whether a paper reports real brine, synthetic brine, or simplified aqueous solution.

## Why Abstracts Cannot Directly Train Reliable ML Models
Abstracts rarely contain complete material descriptors, solution conditions, units, negative results, validation protocols, or repeated experimental data points. Training on abstract-level labels would create severe missing-data bias and unverifiable targets.

## Possible Tasks if 200-500 Experimental Data Points Are Extracted
- Li+ adsorption capacity prediction.
- Li/Mg selectivity prediction.
- Material family classification.
- Regeneration stability prediction.
- Screening of promising lithium adsorbents.
- Descriptor-performance relationship analysis.

## Recommended Models for Small Datasets
- Random forest.
- XGBoost if available.
- Gaussian process regression.
- Support vector regression.
- Ridge/lasso regression.

Deep learning is not recommended unless the data volume and descriptor quality become sufficient.

## Stratified Modeling Recommendation
If material families differ strongly, first train family-specific models or include `material_family` as a categorical feature. Ti-based adsorbents, LDH-based adsorbents, and ion-imprinted polymers should be evaluated separately because their descriptor meanings and mechanisms may differ.
""", encoding="utf-8")


def write_scripts() -> None:
    common = '''from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "lithium_adsorbent_database" / "lithium_adsorbent_structure_performance_template.csv"
OUT = ROOT / "outputs" / "ml_results"
OUT.mkdir(parents=True, exist_ok=True)

def load_data(path=DATA):
    return pd.read_csv(path, dtype=str, encoding="utf-8-sig").replace({"missing": pd.NA, "not available": pd.NA})
'''
    scripts = {
        "clean_lithium_adsorbent_dataset.py": common + '''
def main():
    df = load_data()
    df.to_csv(OUT / "cleaned_lithium_adsorbent_dataset.csv", index=False, encoding="utf-8-sig")
    print(f"Loaded {len(df)} rows. Cleaned template written to {OUT}.")

if __name__ == "__main__":
    main()
''',
        "train_baseline_lithium_adsorbent_models.py": common + '''
def main():
    df = load_data()
    target = "Li_adsorption_capacity_qe"
    if target not in df or df[target].dropna().empty:
        print("No usable target values yet. Extract full-text data before training.")
        return
    from sklearn.model_selection import train_test_split
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    y = pd.to_numeric(df[target], errors="coerce")
    X = df.drop(columns=[target])
    mask = y.notna()
    X, y = X[mask], y[mask]
    cat_cols = X.columns.tolist()
    pre = ColumnTransformer([("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat_cols)])
    model = Pipeline([("pre", pre), ("rf", RandomForestRegressor(n_estimators=300, random_state=42))])
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(Xtr, ytr)
    pred = model.predict(Xte)
    print({"R2": r2_score(yte, pred), "RMSE": mean_squared_error(yte, pred, squared=False), "MAE": mean_absolute_error(yte, pred)})

if __name__ == "__main__":
    main()
''',
        "feature_importance_lithium_adsorbents.py": common + '''
def main():
    print("Feature importance template. Run after baseline model training and verified target extraction.")
    print("Use permutation importance or model-specific importance; use SHAP only if installed and methodologically appropriate.")

if __name__ == "__main__":
    main()
''',
        "plot_lithium_adsorbent_database_statistics.py": common + '''
def main():
    import matplotlib.pyplot as plt
    df = load_data()
    if "material_family" not in df:
        print("material_family column not found.")
        return
    ax = df["material_family"].fillna("missing").value_counts().plot(kind="barh", figsize=(8, 5))
    ax.set_xlabel("Record count")
    ax.set_title("Lithium adsorbent database records by material family")
    plt.tight_layout()
    plt.savefig(OUT / "material_family_counts.png", dpi=300)
    print(f"Saved plot to {OUT / 'material_family_counts.png'}")

if __name__ == "__main__":
    main()
''',
    }
    for name, text in scripts.items():
        (TARGET / "scripts" / name).write_text(text, encoding="utf-8")


def write_readme(docx_found: list[Path], df: pd.DataFrame) -> None:
    (TARGET / "README.md").write_text(f"""# ML_LDH_review

This workspace has been reframed as a lithium adsorbent structure-performance database project for future machine learning and reverse design.

The scope is broader than an ML + LDH review. It includes LDH-based adsorbents, Ti-based and Mn-based lithium ion sieves, Al-based lithium adsorbents, ion-imprinted materials, organic ligand materials, MOF/COF or porous hybrid systems, composites, and selected non-lithium ML-methodology references.

## Current Source Status
- Expected docx abstract files found: {len(docx_found)}
- Initial matrix source: `{SOURCE_MATRIX}`
- Current literature matrix rows: {len(df)}

Do not train final models until full-text experimental data are extracted and verified.
""", encoding="utf-8")


def main() -> None:
    make_dirs()
    docx_found = []
    for base in [TARGET, SOURCE]:
        if base.exists():
            docx_found.extend(base.rglob("*.docx"))
    df = build_literature_matrix()
    write_csv_and_xlsx(df)
    write_classification(df)
    write_database_templates()
    write_notes_and_outputs(df, docx_found)
    write_scripts()
    write_readme(docx_found, df)
    (TARGET / "outputs/build_summary.txt").write_text(
        f"docx_found={len(docx_found)}\nsource_matrix_exists={SOURCE_MATRIX.exists()}\nliterature_records={len(df)}\n",
        encoding="utf-8",
    )
    print(f"Created/updated project: {TARGET}")
    print(f"Literature records: {len(df)}")
    print(f"DOCX files found: {len(docx_found)}")


if __name__ == "__main__":
    main()
