import unittest

import requests

URI = "http://localhost:8983/solr/courses/select"


class TestSolr(unittest.TestCase):

    def setUp(self):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"q": "*:*"}

        self.response = requests.post(URI, data=data, headers=headers)

    def test_up(self):
        """
        Test if query API is up
        """
        self.response.raise_for_status()

    def test_populated(self):
        """
        Test if Solr is populated
        """
        self.assertGreater(len(self.response.json()["response"]["docs"]), 0)


if __name__ == "__main__":
    unittest.main()
