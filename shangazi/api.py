from tastypie.resources import ModelResource
from shangazi.models import Shangazi
from django.utils import timezone
import datetime


class ShangaziResource(ModelResource):
    class Meta:
        # Setting the api meta attributes
        resource_name = "shangazi"
        allowed_methods = ['get']
        excludes = ['publish', 'publish_at', 'created_at', 'id']
        include_resource_uri = False

        queryset = Shangazi.objects.all()

    def get_object_list(self, request):
        # Filters the queryset in meta to get the specific Article required
        timedelta = timezone.now() - datetime.timedelta(days=7)
        query = super(ShangaziResource, self).get_object_list(request)
        query = (query.filter(publish=True).
                 filter(publish_at__lte=timezone.now).
                 filter(publish_at__gte=timedelta).
                 order_by('publish_at'))

        return query

    def alter_list_data_to_serialize(self, request, data_dict):
        # Modifying the data to provide only what is needed in the right
        # form by removing the extra meta variables and editing the
        # dictionary
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])
            if data_dict['objects']:
                a = []
                a.append(data_dict['objects'][0].data["page_1"])
                a.append(data_dict['objects'][0].data["page_2"])
                a.append(data_dict['objects'][0].data["page_3"])
                a.append(data_dict['objects'][0].data["page_4"])
                data_dict['shangazi'] = a
            del data_dict['objects']
        return data_dict
