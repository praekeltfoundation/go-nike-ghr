from django.test import TestCase
from django.core.urlresolvers import reverse
from shangazi.models import Shangazi
from django.utils import timezone
import json


class TestShangaziAPIWorks(TestCase):
    fixtures = ['test/shangazi_api_good_test_data.json']

    def test_api_works(self):
        # Tests to see if API is functioning correctly (however since it
        # is loading json objects the tests will fail in a week from 29-June)
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'shangazi',
                      'api_name': 'api'})
        shangazi = Shangazi.objects.all()
        shangazi.update(created_at=timezone.now(), publish_at=timezone.now())
        response = self.client.get(url)
        self.assertEqual("/vumigo/api/shangazi/", response.request["PATH_INFO"])
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['shangazi'][0],
                         unicode('Test 1'))


class TestAPIShangaziNoNewshangazi(TestCase):
    fixtures = ['test/shangazi_api_non_lastweek_test_data.json']

    def test_no_shangazi_last_week(self):
        # Tests response for no shangazis published in the last 7 days.
        get_fixture = Shangazi.objects.get(pk=1)

        # checking if fixture loads
        self.assertEqual(get_fixture.page_1, unicode("Test 1"))

        # Testing the API
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'shangazi',
                      'api_name': 'api'})

        response = self.client.get(url)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertDictEqual(json.loads(response.content), {})
        self.assertEqual(response.status_code, 200)


class TestAPIShangaziNotPublished(TestCase):
    fixtures = ['test/shangazi_api_unpublished_test_data.json']

    def test_shangazi_not_published(self):
        # Tests to see if shangazis are un-published.
        get_fixture = Shangazi.objects.get(pk=1)

        # checking if fixture loads
        self.assertEqual(get_fixture.page_1, unicode("Test 1"))

        # Testing the API
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'shangazi',
                      'api_name': 'api'})
        response = self.client.get(url)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertDictEqual(json.loads(response.content), {})
        self.assertEqual(response.status_code, 200)
