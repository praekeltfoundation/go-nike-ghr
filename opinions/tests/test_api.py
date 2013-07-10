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
        self.assertEqual(response.request["PATH_INFO"],
                         "/api/opinions/sms/")
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
        print response
