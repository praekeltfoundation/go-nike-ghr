from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class TestOpinion(TestCase):
    fixtures = ['test/test_opinion.json']

    def test_api_works(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'opinion',
                      'api_name': 'api'})

        response = self.client.get(url)
        json_item = json.loads(response.content)
        self.assertEqual(response.request["PATH_INFO"],
                         "/api/opinion/")
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn("opinions", json_item)
        self.assertEqual(json_item["opinions"]["opinion_1"], "A")
