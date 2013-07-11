from models import UserInteraction
from tastypie.resources import ModelResource
from tastypie import http
from tastypie.exceptions import TastypieError
from tastypie.resources import csrf_exempt
from django.utils.cache import patch_cache_control


class UserInteractionResource(ModelResource):
    class Meta:
        resource_name = "userinteraction"
        allowed_methods = ['post']
        list_allowed_methods = ['post']  # Tells API that POST is allowed for base URL
        include_resource_uri = False

    def post_list(self, request, **kwargs):
        """
        Gets posted data so as to save it in the UserInteraction Table
        """
        user_data = request.POST.dict()
        if (len(user_data['msisdn']) > 20):
            raise TastypieError("msisdn Chars are too long, len = %s" % len(user_data['msisdn']))

        if len(user_data['action']) > 200:
            raise TastypieError("action Chars are too long, len = %s" % len(user_data['action']))

        if len(user_data['transport']) > 5:
            raise TastypieError("transport Chars are too long, len = %s" % len(user_data['transport']))

        userinteraction = UserInteraction(msisdn=user_data['msisdn'],
                                          action=user_data['action'],
                                          transport=user_data['transport'])
        userinteraction.save()

    def wrap_view(self, view):
        """
        Wraps views to return custom error code:
        https://gist.github.com/MacMaru/1116962
        """

        @csrf_exempt
        def wrapper(request, *args, **kwargs):
            try:
                callback = getattr(self, view)
                response = callback(request, *args, **kwargs)

                if request.is_ajax():
                    patch_cache_control(response, no_cache=True)
                    pass

                return response

            except TastypieError, e:
                data = {"error": e}
                return self.error_response(request,
                                           data,
                                           response_class=http.HttpBadRequest)
        return wrapper
