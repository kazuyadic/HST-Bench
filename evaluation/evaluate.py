"""Offline HST-Bench evaluation. Python 3.10+; standard library only."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import re

SUBDIMENSIONS=['A1','A2','A3','A4','B1','B2','B3','C1','C2','C3']

def read_jsonl(path):
    with Path(path).open(encoding='utf-8-sig') as f:
        for line_no,line in enumerate(f,1):
            if line.strip():
                try:yield json.loads(line)
                except json.JSONDecodeError as exc:raise ValueError(f'{path}:{line_no}: invalid JSON') from exc

def extract_answer(text):
    """Preserve the archived answer-marker rule; do not guess from free-form prose."""
    match=re.search(r'★答案\s*[:：]\s*([A-D])★',text or '')
    return match.group(1) if match else None

def load_questions(paths):
    out={}
    for path in paths:
        for q in read_jsonl(path):
            key=(str(q['id']),int(q['round']))
            if key in out:raise ValueError(f'Duplicate question/round: {key}')
            if q['subdimension'] not in SUBDIMENSIONS:raise ValueError(f'Unknown subdimension: {key}')
            options=q['options'];labels=[chr(65+i) for i in range(len(options))]
            if q['gold'] not in labels:raise ValueError(f'Invalid gold label: {key}')
            out[key]=q
    return out

def mean(values):
    values=[v for v in values if v is not None]
    return sum(values)/len(values) if values else None

def evaluate(questions,predictions,models=None,score_source='prediction',missing='exclude',rounds=(1,2,3)):
    by_id=defaultdict(dict)
    for (qid,rnd),q in questions.items():
        if rnd in rounds:by_id[qid][rnd]=q
    pred={};discovered=set();ignored=0;mismatches=0;unparsed=defaultdict(int)
    for row in predictions:
        model=row['model'];qid=str(row['id']);rnd=int(row['round']);key=(model,qid,rnd)
        if (qid,rnd) not in questions or rnd not in rounds:ignored+=1;continue
        if key in pred:raise ValueError(f'Duplicate model/question/round: {key}')
        label=row.get('prediction')
        if label is None and 'response' in row:label=extract_answer(row['response'])
        gold=questions[qid,rnd]['gold']
        labels=[chr(65+i) for i in range(len(questions[qid,rnd]['options']))]
        if label not in labels:unparsed[model]+=1
        correct=(label==gold)
        recorded=row.get('recorded_is_correct')
        if isinstance(recorded,bool) and recorded!=correct:mismatches+=1
        if score_source=='recorded':
            if not isinstance(recorded,bool):raise ValueError(f'Missing recorded correctness: {key}')
            correct=recorded
        pred[key]=int(correct);discovered.add(model)
    chosen=sorted(discovered) if models is None else list(models)
    results={}
    for model in chosen:
        groups={s:[] for s in SUBDIMENSIONS};strict_groups={s:[] for s in SUBDIMENSIONS}
        complete=0;answered=0
        for qid,round_questions in by_id.items():
            base=next(iter(round_questions.values()));sub=base['subdimension']
            if any(q['subdimension']!=sub for q in round_questions.values()):
                raise ValueError(f'Inconsistent subdimension across rounds: {qid}')
            vals=[pred.get((model,qid,rnd)) for rnd in rounds]
            available=[v for v in vals if v is not None];answered+=len(available)
            if len(available)==len(rounds) and all(rnd in round_questions for rnd in rounds):
                complete+=1;strict_groups[sub].append(int(all(available)))
            elif missing=='incorrect':strict_groups[sub].append(0)
            if missing=='incorrect':groups[sub].append(sum(available)/len(rounds))
            elif available:groups[sub].append(sum(available)/len(available))
        def summary(group):
            per_type={s:{'n':len(v),'accuracy':mean(v)} for s,v in group.items()}
            all_values=[v for values in group.values() for v in values]
            dimension={d:{'n':sum(len(v) for s,v in group.items() if s.startswith(d)),
                           'micro_accuracy':mean([v for s,vals in group.items() if s.startswith(d) for v in vals]),
                           'macro_subdimension_accuracy':mean([per_type[s]['accuracy'] for s in group if s.startswith(d)])}
                       for d in ['A','B','C']}
            return {'n':len(all_values),'micro_accuracy':mean(all_values),
                    'macro_subdimension_accuracy':mean([x['accuracy'] for x in per_type.values()]),
                    'dimensions':dimension,'subdimensions':per_type}
        results[model]={'recorded_responses':answered,'complete_three_round_questions':complete,
                        'invalid_or_unparsed_responses':unparsed[model],
                        'strict':summary(strict_groups),'mean_attempt':summary(groups)}
    return {'settings':{'rounds':list(rounds),'missing':missing,'score_source':score_source,
                        'accuracy_scale':'fractions in [0, 1], not percentages'},
            'audit':{'question_ids':len(by_id),'prediction_records':len(pred),'ignored_prediction_records':ignored,
                     'recorded_correctness_mismatches':mismatches,
                     'requested_models_without_predictions':[m for m in chosen if m not in discovered]},
            'models':results}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--questions',nargs='+',default=['data/questions_round1.jsonl','data/questions_round2.jsonl','data/questions_round3.jsonl'])
    parser.add_argument('--predictions',default='predictions/archived_predictions.jsonl')
    parser.add_argument('--models-file',type=Path)
    parser.add_argument('--score-source',choices=['prediction','recorded'],default='prediction')
    parser.add_argument('--missing',choices=['exclude','incorrect'],default='exclude')
    parser.add_argument('--output',type=Path,default=Path('results/metrics.json'))
    args=parser.parse_args()
    models=json.loads(args.models_file.read_text(encoding='utf-8')) if args.models_file else None
    result=evaluate(load_questions(args.questions),read_jsonl(args.predictions),models,args.score_source,args.missing)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(f"Evaluated {len(result['models'])} models on {result['audit']['question_ids']} question IDs -> {args.output}")
    if result['audit']['requested_models_without_predictions']:
        print('Models without predictions:',', '.join(result['audit']['requested_models_without_predictions']))

if __name__=='__main__':main()
