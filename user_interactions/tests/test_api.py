from django.test import TestCase
from django.core.urlresolvers import reverse
from user_interactions.models import UserInteraction
import json


class TestUserInteraction(TestCase):

    def test_api_works(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'userinteraction',
                      'api_name': 'api'})
        query = UserInteraction.objects.all()
        self.assertEqual(query.count(), 0)
        response = self.client.post(url,
                                    format="json",
                                    data={"msisdn": "post msisdn",
                                    "feature": "post feature",
                                    "key": "post key",
                                    "value": "post value",
                                    "transport": "sms"})
        self.assertEqual(query.count(), 1)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(query[0].msisdn, "post msisdn")
        self.assertEqual(query[0].feature, "post feature")
        self.assertEqual(query[0].key, "post key")
        self.assertEqual(query[0].value, "post value")
        self.assertEqual(query[0].transport, "sms")

    def test_bad_transport_data(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'userinteraction',
                      'api_name': 'api'})
        response = self.client.post(url,
                                    format="json",
                                    data={"msisdn": "msisdn",
                                    "feature": "post feature",
                                    "key": "post key",
                                    "value": "post value",
                                    "transport": "This is way too long"})
        self.assertEqual(response.status_code, 400)
        json_item = json.loads(response.content)
        self.assertIn("error", json_item)
        self.assertEqual(json_item["error"],
                         "'transport' is longer than the maximum allowed length of 20")

    def test_bad_msisdn_data(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'userinteraction',
                      'api_name': 'api'})
        response = self.client.post(url,
                                    format="json",
                                    data={"msisdn": "msisdnmsisdnmsisdnmsisdn",
                                    "feature": "post feature",
                                    "key": "post key",
                                    "value": "post value",
                                    "transport": "sms"})
        self.assertEqual(response.status_code, 400)
        json_item = json.loads(response.content)
        self.assertIn("error", json_item)
        self.assertEqual(json_item["error"],
                         "'msisdn' is longer than the maximum allowed length of 20")

    def test_bad_feature_data(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'userinteraction',
                      'api_name': 'api'})
        response = self.client.post(url,
                                    format="json",
                                    data={"msisdn": "post msisdn",
                                    "feature": "post feature post feature post feature",
                                    "key": "post key",
                                    "value": "post value",
                                    "transport": "sms"})
        self.assertEqual(response.status_code, 400)
        json_item = json.loads(response.content)
        self.assertIn("error", json_item)
        self.assertEqual(json_item["error"],
                         "'feature' is longer than the maximum allowed length of 30")



class TestU18Filter(TestCase):
    fixtures = ["test/test_userinteraction.json"]

    def test_fixture_loaded(self):
        users = UserInteraction.objects.filter(msisdn=27721231232).all()
        self.assertEqual(sorted([obj.value for obj in users]),
                         sorted([u'Nairobi', u'Female', u'16-18', u'quiz_value']))

        users_2 = UserInteraction.objects.filter(msisdn=27721231231).all()
        self.assertEqual(sorted([obj.value for obj in users_2]),
                         sorted([u'MWOGO', u'16-18', u'Male']))

        users_3 = UserInteraction.objects.filter(msisdn=27721231233).all()
        self.assertEqual(sorted([obj.value for obj in users_3]),
                         sorted([u'25-35', u'CPT', u'Female', u'quiz_value']))

    def test_registered_msisdn_good(self):
        """
        Testing registered MSISDN under 18
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'userinteraction',
                      'api_name': 'api'})

        response = self.client.get("%s?msisdn=27721231232&feature=REGISTRATION"% url)
        json_item = json.loads(response.content)
        self.assertEqual(json_item['U18'], True)

    def test_unregistered_msisdn(self):
        """
        Testing unregistered MSISDN under 18
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'userinteraction',
                      'api_name': 'api'})

        response = self.client.get("%s?msisdn=27721231239&feature=REGISTRATION"% url)
        json_item = json.loads(response.content)
        self.assertEqual(json_item['U18'], False)

    def test_registered_msisdn_over_age(self):
        """
        Testing unregistered MSISDN under 18
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'userinteraction',
                      'api_name': 'api'})

        response = self.client.get("%s?msisdn=27721231233&feature=REGISTRATION"% url)
        json_item = json.loads(response.content)
        self.assertEqual(json_item['U18'], False)


    def test_registered_msisdn_under_age_male(self):
        """
        Testing unregistered MSISDN under 18
        """
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'userinteraction',
                      'api_name': 'api'})

        response = self.client.get("%s?msisdn=27721231231&feature=REGISTRATION"% url)
        json_item = json.loads(response.content)
        self.assertEqual(json_item['U18'], False)
