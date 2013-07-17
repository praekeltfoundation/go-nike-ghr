from django.test import TestCase
from django.core.urlresolvers import reverse
from user_interactions.models import UserInteraction
import json


class TestUserInteraction(TestCase):

    def test_api_works(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'userinteraction',
                      'api_name': 'api'})
        response = self.client.post(url,
                                    format="json",
                                    data={"msisdn": "post msisdn",
                                    "feature": "post feature",
                                    "key": "post key",
                                    "value": "post value",
                                    "transport": "sms"})
        query = UserInteraction.objects.all()
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
