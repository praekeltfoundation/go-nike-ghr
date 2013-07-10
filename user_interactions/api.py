from models import UserInteraction
from tastypie.resources import ModelResource


class UserInteractionResource(ModelResource):
    class Meta:
        resource_name = UserInteraction
        allowed_methods = ['get']
        include_resource_uri = False
