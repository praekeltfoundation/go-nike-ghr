from django.test import TestCase
from django.core.urlresolvers import reverse
from opinions.models import Opinion
import json


class TestOpinion(TestCase):
    def setUp(self):
        Opinion.objects.create(opinion_1="A",
                               opinion_2="B",
                               opinion_3="C",
                               opinion_4="D",
                               opinion_5="E")

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
