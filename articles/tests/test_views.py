from django.test import TestCase
from articles.models import Article
from django.utils import timezone
from django.core.urlresolvers  import reverse
import datetime


class TestAPI(TestCase):
    def setUp(self):
        pass

    def test_api_works(self):
        Article.objects.create(article="Test1",
                               publish=True,
                               publish_at=
                               (timezone.now() - datetime.timedelta(days=8)))

        Article.objects.create(article="Test2",
                               publish=True,
                               publish_at=
                               (timezone.now() - datetime.timedelta(days=5)))

        Article.objects.create(article="Test3",
                               publish=False,
                               publish_at=
                               (timezone.now() + datetime.timedelta(days=18)))

        Article.objects.create(article="Test4",
                               publish=True,
                               publish_at=
                               (timezone.now() + datetime.timedelta(days=3)))

        Article.objects.create(article="Test5",
                               publish=False,
                               publish_at=
                               (timezone.now() - datetime.timedelta(days=2)))

        response = self.client.get("/api/article")
        self.assertEqual("application/json", response["Content-Type"])
        self.assertIn('Test2', response.content)
        self.assertEqual(response.status_code, 200)


    def test_no_article_last_week(self):
        Article.objects.create(article="Test1",
                               publish=True,
                               publish_at=
                               (timezone.now() - datetime.timedelta(days=8)))

        Article.objects.create(article="Test7",
                               publish=True,
                               publish_at=
                               (timezone.now() + datetime.timedelta(seconds=60)))

        response = self.client.get(reverse('articles.views.get_article'))
        self.assertEqual("application/json", response["Content-Type"])
        self.assertIn("Sorry there's no article this week", response.content)
        self.assertEqual(response.status_code, 200)

    def test_article_not_published(self):
        Article.objects.create(article="Test1",
                               publish=False,
                               publish_at=
                               (timezone.now() - datetime.timedelta(days=2)))

        Article.objects.create(article="Test2",
                               publish=False,
                               publish_at=
                               (timezone.now() + datetime.timedelta(days=1)))

        response = self.client.get(reverse('articles.views.get_article'))
        self.assertEqual("application/json", response["Content-Type"])
        self.assertIn("Sorry there's no article this week", response.content)
        self.assertEqual(response.status_code, 200)
