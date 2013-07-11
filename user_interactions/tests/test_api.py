from django.test import TestCase
from django.core.urlresolvers import reverse
from user_interactions.models import UserInteraction


class TestUserInteraction(TestCase):

    def test_api_works(self):
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'userinteraction',
                      'api_name': 'api'})
        response = self.client.post(url, format="json", data={"msisdn": "msisdn",
                                                "action": "action",
                                                "transport": "sms"})

        query = UserInteraction.objects.all()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(query[0].msisdn, "msisdn")
        self.assertEqual(query[0].action, "action")
        self.assertEqual(query[0].transport, "sms")
