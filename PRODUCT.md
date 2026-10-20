# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Python and Streamlit, as stated by the project owner and planned in `app/README.md` (entry point `app/streamlit_app.py`). No application code exists yet.

## Users

The general public in Vietnam ("everyone", per the project owner). No narrower primary segment has been chosen. Users are not assumed to know machine learning or real estate terminology.

## Product Purpose

A public house price estimator for Vietnam. A person enters the details of a house and receives an estimated total price from the team's trained model.

Success means real people can rely on it for a first price estimate, and that it stays usable beyond the AIQS project itself.

## Positioning

Not yet decided. The factual mechanism is an estimate produced by a model trained on the Vietnam Housing Dataset 2024 (30,229 listings). No claim about how this differs from other estimators has been confirmed.

## Operating Context

- The interface language is Vietnamese.
- The user supplies property details by hand; nothing is looked up from an address or a listing.
- The app loads a model pipeline that the team has approved, runs one prediction, and shows the result with its currency unit.

## Capabilities and Constraints

**Inputs (the 12 model features)**

| Feature | Type | Values in the cleaned data |
|---|---|---|
| Area | number | 3.1 – 595 |
| Frontage | number | 0 – 77 |
| Access Road | number | 1 – 85 |
| Floors | whole number | 1 – 10 |
| Bedrooms | whole number | 1 – 9 |
| Bathrooms | whole number | 1 – 9 |
| House direction | category | 8 compass directions |
| Balcony direction | category | 8 compass directions |
| Legal status | category | `Have certificate`, `Sale contract` |
| Furniture state | category | `Full`, `Basic` |
| City | category | 106 distinct strings |
| District | category | 341 distinct strings |

**Output:** `Price`, the total price in tỷ VND (billion VND).

**Constraints**

- The price must be presented as a model estimate that can be wrong, never as a certain value (`app/README.md`).
- The cleaned data only contains prices from 1.0 to 11.5 tỷ VND, so the model has no basis for estimates outside that range.
- The team has not verified whether dataset prices are asking prices or transaction prices; the output must not be called a transaction price.
- Several inputs are often unknown in the data (house direction missing in 70% of rows, balcony direction 83%, furniture state 47%).
- Dataset category values for legal status and furniture state are in English, while the interface is Vietnamese.

**Undecided**

- Which model ships. XGBoost and LightGBM are shortlisted; no model artifact has been saved.
- Units for Area, Frontage and Access Road are not documented in the repository.
- What the app does when Frontage or Access Road is left blank; the cleaned data had these filled before the split and no fitted imputer is saved.
- Whether an error range or interval is shown with the estimate; a calibration split exists but has not been used.
- Product name, deployment target and who maintains the app after the project.

## Evidence on Hand

- Data: `data/_v1.csv` (cleaned, 30,229 rows) and fixed splits in `data/processed/splits_v1/`.
- Validation results in `notebooks/02_baseline_models.ipynb`: Random Forest MAE 1.0239 tỷ VND, R² 0.5982.
- 3-fold cross-validation results in `experiments/model_comparison_cv/recovered_model_cv_summary.csv`: tuned XGBoost MAE 0.9864 tỷ VND, R² 0.6414.
- The team's acceptance target is test R² ≥ 0.7 (`notebooks/01_data_handoff_and_split.ipynb`). The test set has not been evaluated.

Absent, and not to be fabricated: a saved model, final test metrics, prediction intervals, user testimonials, usage numbers, a logo or brand assets, and any real prediction output.

## Product Principles

Derived from the confirmed answers above.

1. **An estimate, stated as one.** Every price is shown as a model estimate with possible error.
2. **Usable by anyone.** Plain Vietnamese, with no machine learning knowledge needed to get a result.
3. **Claim only what the evidence supports.** Accuracy figures come from recorded evaluation, and the limits of the data are stated.
4. **Ask only for what people know.** A person who cannot answer every field should still be able to get an estimate, where the model allows it.
