import os
import shutil
import unittest
from pathlib import Path

import numpy as np
import pytrec_eval

from src.utils import parse_trec_eval, qrels_to_trec, results_to_trec, run_command

METRICS_TO_EVAL = ["map", "P_10"]


class TestTrecEval(unittest.TestCase):

    def setUp(self):
        # Paths to trec_eval data
        self.trec_eval_path = Path("src/trec_eval/trec_eval")

        tmp_path = Path(__file__).parent.joinpath("tmp")
        os.makedirs(tmp_path, exist_ok=True)

        self.results_path = tmp_path.joinpath("results.pri")
        self.qrels_path = tmp_path.joinpath("qrels.pri")

    def tearDown(self):
        shutil.rmtree(self.results_path.parent)

    def test_trec_eval_compare(self):
        """
        Compare two implementations of trec_eval: latest and locally compiled vs python port from https://github.com/cvangysel/pytrec_eval
        """
        # ------------------------------------
        # generate random data
        doc_ids = np.arange(0, 1000)

        qrels = np.random.choice(doc_ids, 150)
        results = np.random.choice(doc_ids, 500)

        qrels = {"q1": {str(x): 1 for x in qrels}}
        results = {"q1": {str(x): np.random.rand() for x in results}}

        # ------------------------------------
        # evaluate with python port
        evaluator = pytrec_eval.RelevanceEvaluator(qrels, {"map", "P_10"})
        scores_1 = evaluator.evaluate(results)["q1"]

        # ------------------------------------
        # evaluate with compiled version
        results_to_trec(results["q1"], output=self.results_path)
        qrels_to_trec(qrels["q1"], output=self.qrels_path)

        stdout = run_command(
            [
                self.trec_eval_path.absolute(),
                self.qrels_path.absolute(),
                self.results_path.absolute(),
            ],
            False,
        )

        scores_2 = parse_trec_eval(stdout)

        # ------------------------------------
        # Compare
        for metric in METRICS_TO_EVAL:
            scr_1 = float(scores_1[metric])
            scr_2 = float(scores_2[metric])
            self.assertAlmostEqual(scr_1, scr_2, 3)


if __name__ == "__main__":
    unittest.main()
