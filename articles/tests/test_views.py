from django.test import TestCase
from articles.models import Article
from django.utils import timezone
import datetime


class TestAPI(TestCase):
    def setUp(self):
        pass

    def test_api_works(self):
        Article.objects.create(article="Test1",
                               publish=True,
                               date_published=
                               (timezone.now() - datetime.timedelta(days=8)))

        Article.objects.create(article="Test2",
                               publish=True,
                               date_published=
                               (timezone.now() - datetime.timedelta(days=5)))

        Article.objects.create(article="Test3",
                               publish=False,
                               date_published=
                               (timezone.now() + datetime.timedelta(days=18)))

        Article.objects.create(article="Test4",
                               publish=True,
                               date_published=
                               (timezone.now() + datetime.timedelta(days=3)))

        Article.objects.create(article="Test5",
                               publish=False,
                               date_published=
                               (timezone.now() - datetime.timedelta(days=2)))

        response = self.client.get("/api/articles/")
        self.assertIn("application/json", response.items()[0])
        self.assertIn('Test2', response.content)
        self.assertEqual(response.status_code, 200)

    def test_no_article_last_week(self):
        Article.objects.create(article="Test1",
                               publish=True,
                               date_published=
                               (timezone.now() - datetime.timedelta(days=8)))

        Article.objects.create(article="Test2",
                               publish=True,
                               date_published=
                               (timezone.now() - datetime.timedelta(days=50)))
        Article.objects.create(article="Test7",
                               publish=True,
                               date_published=
                               (timezone.now() + datetime.timedelta(seconds=60)))

        response = self.client.get("/api/articles/")
        self.assertIn("application/json", response.items()[0])
        self.assertIn("Sorry there's no article this week", response.content)
        self.assertEqual(response.status_code, 200)

    def test_article_not_published(self):
        Article.objects.create(article="Test1",
                               publish=False,
                               date_published=
                               (timezone.now() - datetime.timedelta(days=2)))

        Article.objects.create(article="Test2",
                               publish=False,
                               date_published=
                               (timezone.now() - datetime.timedelta(days=8)))

        Article.objects.create(article="Test7",
                               publish=False,
                               date_published=
                               (timezone.now() + datetime.timedelta(seconds=9)))

        response = self.client.get("/api/articles/")
        self.assertIn("application/json", response.items()[0])
        self.assertIn("Sorry there's no article this week", response.content)
        self.assertEqual(response.status_code, 200)
