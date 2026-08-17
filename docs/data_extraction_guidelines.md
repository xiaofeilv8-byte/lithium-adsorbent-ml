# Data Extraction Guidelines for Lithium Adsorbent Structure-Performance Database

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
