from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class TestMLAPI(TestCase):
    fixtures = ['test/test_M_and_L.json']

    def test_correct_data(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'mandl',
                      'api_name': 'api'})
        response = self.client.get(url)
        self.assertEqual(response.request["PATH_INFO"], "/api/mandl/")
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["quizzes"], [1, 2, 3])

    def test_get_questions(self):
        url = reverse('api_dispatch_detail',
                      kwargs={'resource_name': 'mandl',
                      'api_name': 'api', "pk": 1})
        response = self.client.get(url)
        json_item = json.loads(response.content)
        self.assertEqual(response.request["PATH_INFO"], "/api/mandl/1/")
        self.assertIn("quiz", json_item)

        # Asserying Keys are in data
        self.assertIn("start", json_item["quiz"])
        self.assertIn("q_1", json_item["quiz"]["questions"])
        self.assertIn("q_2", json_item["quiz"]["questions"])
        self.assertIn("q_3", json_item["quiz"]["questions"])
        self.assertIn("q_4", json_item["quiz"]["questions"])

        # Asserting questions
        self.assertEqual(json_item["quiz"]["start"], "q_1")
        self.assertEqual(json_item["quiz"]["questions"]["q_1"]["question"],
                         "Q1A")
        self.assertEqual(json_item["quiz"]["questions"]["q_2"]["question"],
                         "Q1B")
        self.assertEqual(json_item["quiz"]["questions"]["q_3"]["question"],
                         "Q1C")
        self.assertEqual(json_item["quiz"]["questions"]["q_4"]["question"],
                         "Q1D")

        # Asserting the answers
        self.assertEqual(sorted(json_item["quiz"]["questions"]["q_1"]["choices"]),
                         sorted([["q_2", "A1Aa"], ["q_2", "A1Ab"],
                                ["q_2", "A1Ac"]]))

        self.assertEqual(sorted(json_item["quiz"]["questions"]["q_2"]["choices"]),
                         sorted([["q_3", "A1Ba"], ["q_3", "A1Bb"],
                                ["q_3", "A1Bc"]]))

        self.assertEqual(sorted(json_item["quiz"]["questions"]["q_3"]["choices"]),
                         sorted([["q_4", "A1Ca"], ["q_4", "A1Cb"],
                                ["q_4", "A1Cc"]]))

        self.assertEqual(sorted(json_item["quiz"]["questions"]["q_4"]["choices"]),
                         sorted([["main_menu", "A1Da"], ["main_menu", "A1Db"],
                                ["main_menu", "A1Dc"]]))
