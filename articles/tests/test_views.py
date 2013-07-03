from django.test import TestCase
from django.core.urlresolvers import reverse
from articles.models import Article
import json


class TestArticlesAPIWorks(TestCase):
    fixtures = ['test/articles_api_good_test_data.json']

    def test_api_works(self):
        # Tests to see if API is functioning correctly (however since it
        # is loading json objects the tests will fail in a week from 29-June)
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'article',
                      'api_name': 'api'})
        response = self.client.get(url)
        self.assertEqual("/api/article/", response.request["PATH_INFO"])
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['article'][0],
                         unicode('Test 1'))


class TestAPIArticlesNoNewArticle(TestCase):
    fixtures = ['test/articles_api_non_lastweek_test_data.json']

    def test_no_article_last_week(self):
        # Tests response for no articles published in the last 7 days.
        get_fixture = Article.objects.get(pk=1)

        # checking if fixture loads
        self.assertEqual(get_fixture.page_1, unicode("Test 1"))

        # Testing the API
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'article',
                      'api_name': 'api'})

        response = self.client.get(url)
        self.assertEqual("application/json", response["Content-Type"])

        self.assertEqual(json.loads(response.content)['article'],
                         "Sorry there's no article this week, dial back soon!")
        self.assertEqual(response.status_code, 200)


class TestAPIArticlesNotPublished(TestCase):
    fixtures = ['test/articles_api_unpublished_test_data.json']

    def test_article_not_published(self):
        # Tests to see if articles are un-published.
        get_fixture = Article.objects.get(pk=1)

        # checking if fixture loads
        self.assertEqual(get_fixture.page_1, unicode("Test 1"))

        # Testing the API
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'article',
                      'api_name': 'api'})
        response = self.client.get(url)
        self.assertEqual("application/json", response["Content-Type"])
        self.assertEqual(json.loads(response.content)['article'],
                         "Sorry there's no article this week, dial back soon!")
        self.assertEqual(response.status_code, 200)
