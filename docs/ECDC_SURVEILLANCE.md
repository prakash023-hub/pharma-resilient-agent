# ECDC aggregate AMR surveillance

## What this view shows

The app's **ECDC Population Surveillance Trends** panel is a read-only table of annual
country-level percentages of resistant isolates for five single-class series:

- *Escherichia coli*: fluoroquinolones; third-generation cephalosporins
- *Klebsiella pneumoniae*: carbapenems; third-generation cephalosporins
- *Staphylococcus aureus*: meticillin (MRSA)

The two combined-resistance exports supplied with the source files are excluded. The
data is not local hospital antibiogram data, patient-level data, or a treatment
recommendation. It is not sent to `run_pharma_agent` and must not be used to choose an
antibiotic for an individual patient.

## Source, query, and reuse

Source: [ECDC Surveillance Atlas of Infectious Diseases (EARS-Net)](https://atlas.ecdc.europa.eu/).
The exported rows use the indicator `R - resistant isolates, percentage` and unit `%`.
The exact `Population` filters are:

- `Escherichia coli|Fluoroquinolones`
- `Escherichia coli|Third-generation cephalosporins`
- `Klebsiella pneumoniae|Carbapenems`
- `Klebsiella pneumoniae|Third-generation cephalosporins`
- `Staphylococcus aureus|Meticillin (MRSA)`

All available years and regions in the supplied exports were considered; the resulting
snapshot spans 2000–2025 and contains 30 countries. Values are percentages of resistant
isolates, rounded to two decimal places. Rows without a numeric `NumValue` and
combined-resistance indicators are not included.

The source exports did not contain their download date or the Atlas filter/query history.
Their retrieval date is therefore **unknown**; local attachment timestamps are not treated
as source retrieval dates. The files were reviewed on 2026-11-13. Record the actual Atlas
export date and filters when refreshing this snapshot.

ECDC's [intellectual property notice](https://www.ecdc.europa.eu/en/ecdc-intellectual-property-notices)
states that third-party data in ECDC databases may be downloaded and reproduced for
commercial and non-commercial purposes when its source is acknowledged. ECDC requests
this attribution in outputs arising from the data:

> Dataset provided by ECDC based on data provided by public health authorities, scientific
> institutes or health care providers in the relevant reporting countries and/or by WHO.

This project indicates that the data was modified: only the five single-class series were
retained, unreported values were dropped, and percentages were rounded to two decimals.
Third-party restrictions may still apply to identifiable third-party material. The ECDC
logo is not included. The repository's MIT license applies to project code and does not
replace the reuse terms for this dataset.

## Updating the snapshot

1. Download fresh EARS-Net Atlas CSV exports for the same five `Population` values,
   `R - resistant isolates, percentage` indicator, and `%` unit. Keep the date, filters,
   and original exports with the review record.
2. Run `python scripts/build_ecdc_surveillance.py <export.csv> ...` with the five exports.
   The builder maps series from the CSV `Population` values (not filenames), requires all
   five series, validates years/percentages, rejects conflicting duplicate observations,
   and ignores combined-resistance and unreported rows.
3. Review the reported row and ignored-row counts, confirm the official reuse terms still
   apply, and update this document's retrieval date and filter details before committing.
4. Run `python3 -m unittest discover -s tests -v`.

The bundled CSV is a fixed snapshot, not an automatic live feed. Refreshing it must not
change the clinical recommendation path.
