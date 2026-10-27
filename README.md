# HST-Bench

Research data and offline evaluation scripts for the HST-Bench manuscript in preparation for Scientific Reports. This release contains **1,484 unique multiple-choice questions**, three archived option-order rounds, and **102,467 prediction records from 24 model identifiers**. The manuscript model list selects 18 of these identifiers.

## Quick start

Python 3.10 or later is sufficient. There are no third-party dependencies, API calls, or API keys required. Run from the repository root:

```sh
python evaluation/evaluate.py --output results/archived_all_models.json
python evaluation/evaluate.py --models-file config/manuscript_models.json --output results/manuscript_models.json
python -m unittest discover -s tests -v
```

Scores in the JSON output are fractions between 0 and 1. Multiply by 100 to obtain percentages. Inspect the reported denominators: archived model coverage is incomplete and differs between models.

## Contents

| Path | Contents |
| --- | --- |
| `data/questions_round*.jsonl` | 1,484 questions per round, round-specific options and gold labels |
| `predictions/archived_predictions.jsonl` | Lightweight archived model predictions and stored correctness flags |
| `evaluation/evaluate.py` | Offline scoring CLI and answer-marker parser |
| `config/manuscript_models.json` | The 18 manuscript model identifiers |
| `results/` | Recomputed scores for the released inputs |
| `docs/data_manifest.json` | Source archive hashes, category counts and model coverage |
| `docs/annotation_audit.json` | Cross-round consistency and correctness-flag audit |
| `docs/DATA_CARD.md` | Dataset schema, scope and known limitations |
| `docs/EVALUATION.md` | Metric definitions and historical scoring differences |
| `docs/manuscript_tables.tex` | Verbatim snapshots of the two main manuscript tables |
| `docs/HUMAN_BASELINE.md` | Six-person human experiment methods and reported results |
| `human/` | Anonymous participant registry and an empty response-record template |

The release preserves the Chinese question text found in the archives. It does not provide an English translation. Three rounds are repeated presentations of the same questions, not 4,452 independent questions or separate training/test splits.

## Evaluate another model

Create a UTF-8 JSONL file with one record for each question and round:

```json
{"id":"REPLACE_WITH_A_RELEASED_ID","round":1,"model":"my-model","prediction":"A"}
```

Use the IDs and round-specific option ordering from the released question files. Labels are `A` through `D`. Alternatively supply `response` containing the archived marker `★答案：A★`; unparsed responses count as incorrect, while absent records follow the selected missing-data policy.

```sh
python evaluation/evaluate.py --predictions my_predictions.jsonl --output results/my_model.json
```

The archived inference instruction was:

```text
你是一位解题专家,请按以下要求作答：
最后单独一行用★答案：X★格式输出（X为A-D）
示例：
经过计算...
★答案：A★
```

The question and lettered options were appended to this instruction. This release does not reconstruct historical provider settings or guarantee deterministic reproduction of model generations.

## Manuscript results and archived evaluation

The tables in the manuscript are the authoritative reported results. Their numerical values are preserved in `docs/manuscript_tables.tex`; the evaluator does not update or overwrite them. Files under `results/` are separate outputs for the released archived inputs and scoring settings, and are not substitutes for the manuscript tables. The default strict micro score follows the archived three-round strict rule on the filtered question files. Historical averaged spreadsheets used different `a_daluan` inputs and a different aggregation; scores computed here from filtered data should not be presented as reproducing those spreadsheets. See [evaluation details](docs/EVALUATION.md).

The authors confirm that six graduate students completed the human-baseline experiment. The six-person study design, reported results, participant registry and response-record template are documented in [HUMAN_BASELINE.md](docs/HUMAN_BASELINE.md). Identifying information, full model reasoning, provider credentials and local configuration are excluded. Questions were collected from Internet sources; see the concise [source and rights notice](LICENSE.md).

## Citation and contact

Bibliographic metadata are in `CITATION.cff`. No DOI or accepted publication is claimed. Corresponding author: Tianwei Yan, augusyan@hotmail.com.

中文说明：本仓库提供论文相关的 1,484 道题、三轮选项排列、归档模型预测及离线评估代码。论文表格作为正式报告结果，数值保持不变；`results/` 仅为归档输入的脚本输出。作者已确认六位研究生完成了人工实验，本仓库补充了六人实验方法、匿名编号和逐题记录模板。题目来自互联网收集，原始材料权利归相应权利人。
