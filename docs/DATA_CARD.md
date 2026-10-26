# Dataset card

## Scope

HST-Bench contains 1,484 unique Chinese multiple-choice questions, each with four options. The three released rounds preserve archived option permutations. All rounds have the same question IDs; question text, option contents and correct-answer contents were checked across rounds. This consistency audit does not independently verify the scientific correctness of each gold answer.

| Dimension | Question count |
| --- | ---: |
| A: Representational Perception | 678 |
| B: Representational Transformation | 356 |
| C: Spatial Reasoning | 450 |

The subdimensions contain A1:170, A2:170, A3:177, A4:161, B1:119, B2:134, B3:103, C1:150, C2:150, C3:150 questions. Subject labels cover physics (512), mathematics (413), aeronautics (146), navigation (237), astronomy (102), and IQ (74). Answer-type counts are numerical (987), symbolic (310), and non-calculation (187).

## Question schema

Each line of `data/questions_roundN.jsonl` is an object:

| Field | Meaning |
| --- | --- |
| `id` | Archived question identifier, serialized as a string |
| `round` | 1, 2 or 3 |
| `question` | Archived Chinese question text |
| `options` | Four answer texts in the order corresponding to A, B, C, D |
| `gold` | Correct option letter for this round |
| `dimension`, `subdimension` | A/B/C and A1–C3 |
| `type_name` | Archived Chinese subtype name |
| `subject`, `answer_type` | Archived subject and answer-type labels |

The prediction file uses `id`, `round`, `model`, `prediction`, and, where present, `recorded_is_correct`. Prediction labels are archived model answers; malformed or unknown labels remain visible to the evaluator. Do not assume the predicted label is the gold answer.

## Provenance and preparation

The release was extracted from the archived `a_filtered1.json`, `a_filtered2.json` and `a_filtered3.json` files. Original file sizes and SHA-256 hashes are recorded in `data_manifest.json`. The earlier 1,629-item unfiltered dataset is outside this release. Extraction retains question text, options, gold labels, classification fields and compact predictions. It omits full model reasoning, intermediate processing fields, internal machine paths, provider credentials and human identities.

## Known limitations and pending information

- This archive contains 24 model identifiers; the manuscript selection contains 18. Coverage varies by model and round. Missing records must not be silently treated as successful predictions.
- The released question text is Chinese. No translated dataset or independent translation validation is included.
- No predefined training/development/test split is provided. The three rounds are repeated evaluation presentations.
- The authors confirm that six graduate students completed the human-baseline experiment. Its methods and reported results are documented in `HUMAN_BASELINE.md`.
- Questions were collected from Internet sources, as reported by the authors. Original material rights remain with the respective rights holders; see `LICENSE.md`.
- Independent gold-label adjudication, contamination assessment and a fully specified historical model-generation environment are not provided.
- Manuscript tables are preserved as the authoritative reported results. Archived evaluator outputs are provided separately and do not establish exact reproduction of those tables.

Use this release to inspect and recompute the archived evaluation. Its scores alone do not establish validity for educational assessment, human ability measurement or other consequential use.
