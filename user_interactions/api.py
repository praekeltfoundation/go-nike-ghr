from models import UserInteraction
from tastypie.resources import ModelResource


class UserInteractionResource(ModelResource):
    class Meta:
        resource_name = "userinteraction"
        allowed_methods = ['post']
        list_allowed_methods = ['post']
        include_resource_uri = False
        # queryset = UserInteraction.objects.all()

    def post_list(self, request, **kwargs):
        user_data = request.POST.dict()
        userinteraction = UserInteraction(msisdn=user_data['msisdn'],
                                          action=user_data['action'],
                                          transport=user_data['transport'])
        userinteraction.save()
