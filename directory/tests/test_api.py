from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class TestCategoryApi(TestCase):
    fixtures = ['test/test_weekly_quiz.json']

    def test_correct_url(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'category',
                      'api_name': 'api'})
        response = self.client.get(url)
        self.assertEqual(response.request["PATH_INFO"], "/api/category/")
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
