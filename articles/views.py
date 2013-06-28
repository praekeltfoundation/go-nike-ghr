from django.http import HttpResponse
from articles.models import Article
import json
from django.utils import timezone
import datetime


def get_article(request):
    timedelta = timezone.now() - datetime.timedelta(days=7)

    queryset = (Article.objects.all().
                filter(publish=True).
                filter(publish_at__lte=timezone.now).
                filter(publish_at__gte=timedelta).
                order_by('publish_at'))

    if queryset.exists():
        output = {"article": queryset[0].article}
    else:
        output = {"article":
                  "Sorry there's no article this week, dial back soon!"}

    return HttpResponse(json.dumps(output),
                        content_type="application/json")
