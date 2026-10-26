# Evaluation definitions

## Correctness and parsing

By default, correctness is recomputed as predicted option letter equals the gold letter for the same question ID and round. A provided `prediction` takes precedence; when it is null or absent, `response` can be parsed using `★答案\s*[:：]\s*([A-D])★`. Unparsed or invalid supplied answers are incorrect. `--score-source recorded` instead uses the archived boolean `recorded_is_correct` and fails if that field is missing.

Duplicate model/question/round records and duplicate question/round records are rejected. Predictions for unknown question/round combinations are ignored and counted in the output audit. The audit also counts discrepancies between stored correctness flags and recomputed labels. The released archive has zero such discrepancies.

## Metrics

For each model and question, let c(r) be 1 for a correct response in round r and 0 otherwise.

- `strict`: a question receives 1 only if all three rounds are correct.
- `mean_attempt`: a question receives the arithmetic mean of its available round correctness values under the default missing-data policy.
- `micro_accuracy`: arithmetic mean of eligible question scores, with each question having equal weight.
- `macro_subdimension_accuracy`: arithmetic mean of available subtype accuracies, with each nonempty subtype having equal weight. Dimension summaries use only subtypes belonging to that dimension.

Subtype entries contain `n` and `accuracy`; dimension and overall entries contain their denominator `n`. Empty groups return JSON null accuracy, not zero. All scores are fractions rather than percentages. The output reports per-model response counts, complete-three-round counts and invalid/unparsed response counts.

## Missing responses

Default `--missing exclude` matches the archived strict script's exclusion behavior: strict scores require all three responses and otherwise omit that question for the model. Mean-attempt scores use available rounds and omit questions with no responses. Consequently their denominators can differ.

With `--missing incorrect`, missing responses contribute zero, strict questions with missing rounds are incorrect, and all question IDs in the loaded selected rounds enter each model's denominator. This provides a fixed-question-denominator alternative. The policy is saved in the result settings.

## Historical scripts and manuscript reconciliation

The archived `static_cirlce.py` used the three filtered files, required three responses, and computed strict micro accuracy. Its hard-coded model list included 17 models and omitted `qwen2.5-7b`. The new evaluator includes all 24 archived identifiers by default; `config/manuscript_models.json` selects the manuscript's 18 identifiers. Compare the shared model IDs when validating historical strict results.

The archived `static_avg.py` read three `a_daluan` files, allowed partial rounds, averaged correctness within each question and subtype, and then equally averaged subtype accuracies. That input dataset is not the three filtered files in this release. The new evaluator exposes a mean-attempt macro-subdimension score, but computing it on released filtered inputs does not reproduce those historical averaged spreadsheets by itself.

The manuscript tables are the authoritative reported results and are preserved without recalculation in `manuscript_tables.tex`. The committed `results/` files describe only the released inputs and settings. They do not replace manuscript values or demonstrate exact table reproduction. The authors confirm completion of the six-person human experiment; its protocol is documented in `HUMAN_BASELINE.md`.
