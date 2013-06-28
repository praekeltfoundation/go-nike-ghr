from tastypie.resources import ModelResource
from articles.models import Article
from django.utils import timezone
import datetime
import copy


class ArticleResource(ModelResource):
    class Meta:
        resource_name = "article"
        allowed_methods = ['get']
        excludes = ['publish', 'publish_at', 'created_at', 'id']
        include_resource_uri = False

        queryset = Article.objects.all()

    def get_object_list(self, request):
        timedelta = timezone.now() - datetime.timedelta(days=7)
        query = super(ArticleResource, self).get_object_list(request)
        query = (query.filter(publish=True).
                 filter(publish_at__lte=timezone.now).
                 filter(publish_at__gte=timedelta).
                 order_by('publish_at'))

        if query.exists():
            return query
        else:
            return Article.objects.none()

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])
            if data_dict['objects'] == []:
                del (data_dict['objects'])
                data_dict['article'] = "Sorry there's no article this week, dial back soon!"
            else:
                data_dict['article'] = copy.copy(data_dict['objects'][0].data['article'])
                del (data_dict['objects'])
        return data_dict
