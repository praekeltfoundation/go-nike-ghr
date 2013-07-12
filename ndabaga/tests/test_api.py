from django.test import TestCase
from django.core.urlresolvers import reverse
from ndabaga.models import Ndabaga
import json


class TestNdabagaAPIWorks(TestCase):
    fixtures = ['test/ndabaga_api_good_test_data.json']

    def test_api_works(self):
        # Tests to see if API is functioning correctly (however since it
        # is loading json objects the tests will fail in a week from 29-June)
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'ndabaga',
                      'api_name': 'api'})
        response = self.client.get(url)
        self.assertEqual("/api/ndabaga/", response.request["PATH_INFO"])
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['ndabaga'][0],
                         unicode('Test 1'))


class TestAPINdabagaNoNewNdabaga(TestCase):
    fixtures = ['test/ndabaga_api_non_lastweek_test_data.json']

    def test_no_ndabaga_last_week(self):
        # Tests response for no ndabagas published in the last 7 days.
        get_fixture = Ndabaga.objects.get(pk=1)

        # checking if fixture loads
        self.assertEqual(get_fixture.page_1, unicode("Test 1"))

        # Testing the API
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'ndabaga',
                      'api_name': 'api'})

        response = self.client.get(url)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertDictEqual(json.loads(response.content), {})
        self.assertEqual(response.status_code, 200)


class TestAPINdabagaNotPublished(TestCase):
    fixtures = ['test/ndabaga_api_unpublished_test_data.json']

    def test_ndabaga_not_published(self):
        # Tests to see if ndabagas are un-published.
        get_fixture = Ndabaga.objects.get(pk=1)

        # checking if fixture loads
        self.assertEqual(get_fixture.page_1, unicode("Test 1"))

        # Testing the API
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'ndabaga',
                      'api_name': 'api'})
        response = self.client.get(url)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertDictEqual(json.loads(response.content), {})
        self.assertEqual(response.status_code, 200)
