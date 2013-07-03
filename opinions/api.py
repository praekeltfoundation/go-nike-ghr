from tastypie.resources import ModelResource
from opinions.models import Opinion
from django.utils import timezone
import datetime
import copy

class OpinionResource(ModelResource):
    class Meta:
        # Setting the api meta attributes
        resource_name = "article"
        allowed_methods = ['get']
        excludes = ['publish', 'publish_at', 'created_at', 'id']
        include_resource_uri = False

        queryset = Opinion.objects.all()

    def alter_list_data_to_serialize(self, request, data_dict):
        # Modifying the data to provide only what is needed in the right
        # form by removing the extra meta variables and editing the
        # dictionary
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])

            data_dict['opinion'] = (copy.copy(data_dict['objects'][0].
                                    data['opinion']))
            del (data_dict['objects'])
        return data_dict
