from models import UserInteraction
from tastypie.resources import ModelResource
from tastypie import http, fields
from tastypie.exceptions import TastypieError, BadRequest
from tastypie.resources import csrf_exempt
from django.utils.cache import patch_cache_control
from django.core.exceptions import ValidationError


class UserInteractionResource(ModelResource):
    class Meta:
        resource_name = "userinteraction"
        allowed_methods = ['post']
        list_allowed_methods = ['post']  # POST is allowed for base URL
        include_resource_uri = False

    def post_list(self, request, **kwargs):
        """
        Gets posted data so as to save it in the UserInteraction Table, but
        checks if the characters are not too long (if this is not done TastyPie
        returns a huge annoying error)
        """
        user_data = request.POST.dict()
        if (len(user_data['msisdn']) > 20):
            raise TastypieError("msisdn Chars are too long, len = %s"
                                % len(user_data['msisdn']))

        if len(user_data['feature']) > 30:
            raise TastypieError("feature Chars are too long, len = %s"
                                % len(user_data['feature']))

        if len(user_data['key']) > 100:
            raise TastypieError("key Chars are too long, len = %s"
                                % len(user_data['key']))

        if len(user_data['value']) > 200:
            raise TastypieError("value Chars are too long, len = %s"
                                % len(user_data['value']))

        if len(user_data['transport']) > 5:
            raise TastypieError("transport Chars are too long, len = %s"
                                % len(user_data['transport']))

        userinteraction = UserInteraction(msisdn=user_data['msisdn'],
                                          feature=user_data['feature'],
                                          key=user_data['key'],
                                          value=user_data['value'],
                                          transport=user_data['transport'])
        userinteraction.save()

    def wrap_view(self, view):
        """
        Wraps views to return custom error code:
        https://gist.github.com/MacMaru/1116962
        """

        @csrf_exempt
        def wrapper(request, *args, **kwargs):
            """
            This function specifically catches the error too long exception
            """
            try:
                callback = getattr(self, view)
                response = callback(request, *args, **kwargs)

                if request.is_ajax():
                    patch_cache_control(response, no_cache=True)
                return response

            except TastypieError, e:
                data = {"error": e}
                return self.error_response(request,
                                           data,
                                           response_class=http.HttpBadRequest)

            except (BadRequest, fields.ApiFieldError), e:
                data = {"error": e.args[0] if getattr(e, 'args') else ''}
                return self.error_response(request, data, response_class=http.HttpBadRequest)

            except ValidationError, e:
                data = {"error": e.messages}
                return self.error_response(request, data, response_class=http.HttpBadRequest)

            except Exception, e:
                if hasattr(e, 'response'):
                    return e.response

                return self._handle_500(request, e)

        return wrapper
