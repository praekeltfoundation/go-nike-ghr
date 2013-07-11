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
                                    data={"msisdn": "msisdn",
                                    "action": "action",
                                    "transport": "sms"})

        query = UserInteraction.objects.all()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(query[0].msisdn, "msisdn")
        self.assertEqual(query[0].action, "action")
        self.assertEqual(query[0].transport, "sms")

    def test_bad_transport_data(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'userinteraction',
                      'api_name': 'api'})
        response = self.client.post(url,
                                    format="json",
                                    data={"msisdn": "msisdn",
                                    "action": "action",
                                    "transport": "This is way too long"})
        self.assertEqual(response.status_code, 400)
        json_item = json.loads(response.content)
        self.assertIn("error", json_item)
        self.assertEqual(json_item["error"],
                         "transport Chars are too long, len = 20")

    def test_bad_msisdn_data(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'userinteraction',
                      'api_name': 'api'})
        response = self.client.post(url,
                                    format="json",
                                    data={"msisdn": "msisdnmsisdnmsisdnmsisdn",
                                    "action": "action",
                                    "transport": "sms"})
        self.assertEqual(response.status_code, 400)
        json_item = json.loads(response.content)
        self.assertIn("error", json_item)
        self.assertEqual(json_item["error"],
                         "msisdn Chars are too long, len = 24")
