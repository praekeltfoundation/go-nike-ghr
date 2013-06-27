from django.http import HttpResponse
from articles.models import Article
from django.utils import simplejson
from django.utils import timezone
import datetime


def get_articles(request):
    timedelta = timezone.now() - datetime.timedelta(days=7)
    try:
        queryset = (Article.objects.all().
                    filter(publish=True).
                    filter(publish_at__lte=timezone.now()).
                    filter(publish_at__gte=timedelta).
                    order_by('publish_at')[0])
        output = {"article": queryset.article}
    except IndexError:
        output = {"article":
                  "Sorry there's no article this week, dial back soon!"}

    return HttpResponse(simplejson.dumps(output),
                        content_type="application/json")
