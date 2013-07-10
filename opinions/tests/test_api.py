from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class TestOpinion(TestCase):
    fixtures = ['test/test_opinion.json']

    def test_api_works(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'opinions/sms',
                      'api_name': 'api'})

        response = self.client.get(url)
        json_item = json.loads(response.content)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn("opinions", json_item)
        self.assertEqual(json_item["opinions"]["opinion_1"], "A")


class TestOpinionPolls(TestCase):
    fixtures = ['test/test_opinion_poll.json']

    def test_opinion_polls_url(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'opinions/view',
                      'api_name': 'api'})
        response = self.client.get(url)
        json_item = json.loads(response.content)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn("opinions", json_item)
        self.assertEqual(sorted(['opinion_view_1', 'opinion_view_2']),
                         sorted([k for k in json_item["opinions"]]))

        self.assertEqual(sorted(['start', 'views']),
                         sorted([k for k in json_item["opinions"]['opinion_view_1']]))

        self.assertEqual('o_1', json_item["opinions"]['opinion_view_1']["start"])
        self.assertEqual('o_2', json_item["opinions"]['opinion_view_2']["start"])

        self.assertEqual(sorted(['o_2', 'o_3']),
                         sorted([k for k in json_item["opinions"]['opinion_view_2']["views"]]))

        self.assertEqual(sorted(['opinions', 'choices']),
                         sorted([k for k in json_item["opinions"]['opinion_view_2']["views"]["o_2"]]))

        self.assertEqual('O2A', json_item["opinions"]['opinion_view_2']["views"]['o_2']['opinions'])

        self.assertEqual(sorted([['o_3', 'C2Aa'], ['o_3', 'C2Ab']]),
                         sorted([k for k in json_item["opinions"]['opinion_view_2']["views"]["o_2"]['choices']]))

        self.assertEqual('O2B', json_item["opinions"]['opinion_view_2']["views"]['o_3']['opinions'])

        self.assertEqual(sorted([['main_menu', 'C2Ba'], ['main_menu', 'C2Bb'], ['main_menu', 'C2Bc']]),
                         sorted([k for k in json_item["opinions"]['opinion_view_2']["views"]["o_3"]['choices']]))
