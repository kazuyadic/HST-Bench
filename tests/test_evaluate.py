import unittest
from evaluation.evaluate import evaluate,extract_answer

def question(rnd,gold='A'):
    return {'id':'q1','round':rnd,'gold':gold,'options':['first','second','third','fourth'],'dimension':'A','subdimension':'A1'}

class EvaluationTests(unittest.TestCase):
    def test_round_specific_gold_and_strict_vs_average(self):
        questions={('q1',r):question(r,gold) for r,gold in [(1,'A'),(2,'B'),(3,'C')]}
        predictions=[{'id':'q1','round':r,'model':'m','prediction':p} for r,p in [(1,'A'),(2,'B'),(3,'A')]]
        result=evaluate(questions,predictions)['models']['m']
        self.assertEqual(result['strict']['micro_accuracy'],0)
        self.assertAlmostEqual(result['mean_attempt']['micro_accuracy'],2/3)

    def test_missing_response_is_excluded_from_strict(self):
        questions={('q1',r):question(r) for r in [1,2,3]}
        predictions=[{'id':'q1','round':r,'model':'m','prediction':'A'} for r in [1,2]]
        result=evaluate(questions,predictions)['models']['m']
        self.assertIsNone(result['strict']['micro_accuracy'])
        self.assertEqual(result['mean_attempt']['micro_accuracy'],1)
        counted=evaluate(questions,predictions,missing='incorrect')['models']['m']
        self.assertEqual(counted['strict']['micro_accuracy'],0)
        self.assertAlmostEqual(counted['mean_attempt']['micro_accuracy'],2/3)

    def test_duplicate_predictions_rejected(self):
        q={('q1',1):question(1)};p={'id':'q1','round':1,'model':'m','prediction':'A'}
        with self.assertRaises(ValueError):evaluate(q,[p,p])

    def test_recorded_score_disagreement_is_visible(self):
        q={('q1',r):question(r) for r in [1,2,3]}
        p=[{'id':'q1','round':r,'model':'m','prediction':'B','recorded_is_correct':True} for r in [1,2,3]]
        result=evaluate(q,p)
        self.assertEqual(result['audit']['recorded_correctness_mismatches'],3)
        self.assertEqual(result['models']['m']['strict']['micro_accuracy'],0)
        self.assertEqual(evaluate(q,p,score_source='recorded')['models']['m']['strict']['micro_accuracy'],1)

    def test_answer_format(self):
        self.assertEqual(extract_answer('推理\n★答案：C★'),'C')
        self.assertIsNone(extract_answer('I think C'))

if __name__=='__main__':unittest.main()
