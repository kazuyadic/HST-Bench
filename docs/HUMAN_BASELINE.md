# Six-person human baseline

## Study completion and reporting

Six graduate students completed the human-baseline experiment.

The study design below is transcribed from the accompanying manuscript and Supplementary Section S6. Manuscript table values remain the authoritative reported results and have not been recalculated for this documentation update.

## Participants and allocation

Six graduate students with STEM backgrounds participated. The manuscript assigns them to two groups of three: Group A comprises A1, A2 and A3; Group B comprises A4, A5 and A6. These are anonymous participant identifiers. Dataset-curation annotation by four students is a separate procedure and should not be confused with this six-person baseline.

According to the manuscript, 200 benchmark questions were selected by stratified random sampling, with 100 allocated to each group. Each participant answered their group's questions independently. Supplementary Section S6 describes isolated annotation, no communication between participants, and blinded evaluation.

## Scoring protocol in the manuscript

For participant Ai, include only questions for which the other two participants in the same group agree on their option label. Compare Ai's answer with the verified question gold label on this eligible set. If Ni is its size, participant accuracy is:

```text
accuracy_i = 100 * number of correct eligible responses / Ni
human_baseline = (accuracy_1 + ... + accuracy_6) / 6
```

This is an equally weighted mean of six participant accuracies, not pooled accuracy over all responses. Eligibility depends on agreement of the other two participants; their agreement is not itself substituted for the gold label. If Ni is zero, the participant score is undefined and must not be silently set to zero or excluded from the six-person mean.

## Reported manuscript values

| Manuscript category | Reported accuracy (%) |
| --- | ---: |
| A: Representational Perception | 76.9 |
| B: Representational Transformation | 87.4 |
| C: Spatial Reasoning | 81.0 |
| Overall | 80.1 |

These values are taken from the manuscript's human-baseline row.

## Record format

`human/participant_registry.csv` lists the six anonymous identifiers and group assignments described in the manuscript. `human/response_template.csv` provides the column format for response records.

For each original response, record participant ID, group, question ID, round (if applicable), option texts in their displayed order, response label, gold label and source record ID. Preserve displayed option order: label A in one permutation need not refer to the same answer text in another.
