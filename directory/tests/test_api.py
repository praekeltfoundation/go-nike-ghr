from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class TestCategoryApi(TestCase):
    fixtures = ['test_directory.json']

    def test_correct_url(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'category',
                      'api_name': 'api'})
        response = self.client.get(url)
        self.assertEqual(response.request["PATH_INFO"], "/api/category/")
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)

    def test_api_response(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'category',
                      'api_name': 'api'})
        response = self.client.get(url)
        json_item = json.loads(response.content)

        self.assertIn("directory", json_item)
        self.assertIn("C1", json_item["directory"])
        self.assertIn("C2", json_item["directory"])
        self.assertIn("SC1A", json_item["directory"]["C1"])
        self.assertIn("SC1B", json_item["directory"]["C1"])

        self.assertDictEqual(json_item["directory"]["C1"]["SC1A"],
                             {"content_3": "C1Ac", "content_2": "C1Ab", "content_1": "C1Aa", })

        self.assertDictEqual(json_item["directory"]["C1"]["SC1B"],
                             {"content_3": "C1Ba", "content_2": "C1Ba", "content_1": "C1Ba", })
