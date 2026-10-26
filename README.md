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

## Reproducibility status

This is an archival data and evaluator release. It is **not a certification that every manuscript table has been reproduced**. The default strict micro score follows the archived three-round strict rule on the filtered question files. Historical averaged spreadsheets used different `a_daluan` inputs and a different aggregation; scores computed here from filtered data should not be presented as reproducing those spreadsheets. See [evaluation details](docs/EVALUATION.md).

Human participant annotations, identifying information, full model reasoning, provider credentials and local configuration are excluded. Six-person human-baseline results cannot be recomputed from this package. Item-level source provenance, redistribution permissions and the final dataset/code licenses remain to be completed by the authors; see [LICENSE.md](LICENSE.md).

## Citation and contact

Bibliographic metadata are in `CITATION.cff`. No DOI or accepted publication is claimed. Corresponding author: Tianwei Yan, augusyan@cqjtu.edu.cn.

中文说明：本仓库提供论文相关的 1,484 道题、三轮选项排列、归档模型预测及离线评估代码。运行不需要模型接口或密钥。模型缺失记录、严格三轮评分和平均评分的口径见文档；当前材料不包含可重算六人基线的完整人工标注。题目来源授权、正式许可证和论文表格复核仍待作者补全。
