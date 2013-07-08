from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class TestWeeklyQuizApi(TestCase):
    fixtures = ['test/test_weekly_quiz.json']

    def test_correct_url(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'weeklyquiz',
                      'api_name': 'api'})
        response = self.client.get(url)
        self.assertEqual(response.request["PATH_INFO"], "/api/weeklyquiz/")
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)

    def test_api_response(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'weeklyquiz',
                      'api_name': 'api'})
        response = self.client.get(url)
        json_item = json.loads(response.content)

        self.assertIn("quiz", json_item)
        self.assertIn("start", json_item["quiz"])
        self.assertIn("quiz_details", json_item["quiz"])
        self.assertIn("questions", json_item["quiz"]["quiz_details"])
        self.assertIn("answers", json_item["quiz"]["quiz_details"])
        self.assertIn("q_6", json_item["quiz"]["quiz_details"]["questions"])
        self.assertIn("q_7", json_item["quiz"]["quiz_details"]["questions"])
        self.assertIn("q_8", json_item["quiz"]["quiz_details"]["questions"])

        self.assertEqual(json_item["quiz"]["start"], "q_6")

        self.assertEqual(json_item["quiz"]["quiz_details"]["questions"]["q_6"]["question"],
                         "Q21")
        self.assertEqual(json_item["quiz"]["quiz_details"]["questions"]["q_7"]["question"],
                         "Q22")
        self.assertEqual(json_item["quiz"]["quiz_details"]["questions"]["q_8"]["question"],
                         "Q23")

        # Asserting the answers
        self.assertEqual(sorted(json_item["quiz"]["quiz_details"]["questions"]["q_6"]["choices"]),
                         sorted([["q_6_a_16", "A21a"], ["q_6_a_17", "A21b"],
                                ["q_6_a_18", "A21c"]]))

        self.assertEqual(sorted(json_item["quiz"]["quiz_details"]["questions"]["q_7"]["choices"]),
                         sorted([["q_7_a_19", "A22a"], ["q_7_a_20", "A22b"],
                                ["q_7_a_21", "A22c"]]))

        self.assertEqual(sorted(json_item["quiz"]["quiz_details"]["questions"]["q_8"]["choices"]),
                         sorted([["q_8_a_22", "A23a"], ["q_8_a_23", "A23b"],
                                ["q_8_a_24", "A23c"]]))

        # Asserting The Answers
        self.assertDictEqual(json_item["quiz"]["quiz_details"]["answers"]["q_6_a_16"],
                             {"response": "R21a", "next": "q_7"})

        self.assertDictEqual(json_item["quiz"]["quiz_details"]["answers"]["q_6_a_17"],
                             {"response": "R21b", "next": "q_7"})

        self.assertDictEqual(json_item["quiz"]["quiz_details"]["answers"]["q_6_a_18"],
                             {"response": "R21c", "next": "q_7"})

        self.assertDictEqual(json_item["quiz"]["quiz_details"]["answers"]["q_7_a_19"],
                             {"response": "R22a", "next": "q_8"})

        self.assertDictEqual(json_item["quiz"]["quiz_details"]["answers"]["q_7_a_20"],
                             {"response": "R22b", "next": "q_8"})

        self.assertDictEqual(json_item["quiz"]["quiz_details"]["answers"]["q_7_a_21"],
                             {"response": "R22c", "next": "q_8"})

        self.assertDictEqual(json_item["quiz"]["quiz_details"]["answers"]["q_8_a_22"],
                             {"response": "R23a", "next": "main_menu"})

        self.assertDictEqual(json_item["quiz"]["quiz_details"]["answers"]["q_8_a_23"],
                             {"response": "R23b", "next": "main_menu"})

        self.assertDictEqual(json_item["quiz"]["quiz_details"]["answers"]["q_8_a_24"],
                             {"response": "R23c", "next": "main_menu"})

class TestWeeklyQuizApiNotActive(TestCase):
    fixtures = ['test/test_weekly_quiz_inactive.json']

    def test_api_response(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'weeklyquiz',
                      'api_name': 'api'})
        response = self.client.get(url)
        json_item = json.loads(response.content)
        self.assertEqual(json_item["quiz"], False)
