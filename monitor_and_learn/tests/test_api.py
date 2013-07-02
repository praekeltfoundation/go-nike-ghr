from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class TestMLAPI(TestCase):
    fixtures = ['test/test_M_and_L.json']

    def test_correct_url(self):
        response = self.client.get('/api/mandl/1/')
        print response
        self.assertEqual(response.status_code, 200)
        

    # def test_correct_data(self):
    #     url = reverse('api_dispatch_list',
    #                   kwargs={'resource_name': 'mandl',
    #                   'api_name': 'api'})

    #     response = self.client.get(url)
    #     self.assertEqual("application/json", response["Content-Type"])
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content)["quizzes"], [1, 2, 3])
