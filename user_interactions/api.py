from models import UserInteraction
from tastypie.resources import ModelResource


class UserInteractionResource(ModelResource):
    class Meta:
        resource_name = "userinteraction"
        allowed_methods = ['post']
        list_allowed_methods = ['post']  # Tells API that POST is allowed for base URL
        include_resource_uri = False

    def post_list(self, request, **kwargs):
        """
        Gets posted data and stores it the the UserInteraction Table
        """
        user_data = request.POST.dict()
        userinteraction = UserInteraction(msisdn=user_data['msisdn'],
                                          action=user_data['action'],
                                          transport=user_data['transport'])
        userinteraction.save()
