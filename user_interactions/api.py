from models import UserInteraction
from tastypie.resources import ModelResource, ALL
from tastypie import http, fields
from tastypie.exceptions import TastypieError, BadRequest
from tastypie.resources import csrf_exempt
from django.utils.cache import patch_cache_control
from django.core.exceptions import ValidationError


class UserInteractionResource(ModelResource):
    """
        To get specific filtering for age use
            /api/userinteraction/?msisdn=27721231232&feature=REGISTRATION
    """
    class Meta:
        resource_name = "userinteraction"
        allowed_methods = ['post', 'get']
        list_allowed_methods = ['post', 'get']  # POST is allowed for base URL
        include_resource_uri = False
        queryset = UserInteraction.objects.all()
        filtering = {
            'msisdn': ALL,
            'feature': ALL}


    def alter_list_data_to_serialize(self, request, data_dict):
        """
        overiding tastypie function that returns data in required format
        """
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del data_dict['meta']
            if data_dict["objects"] == []:
                data_dict['U18'] = False
                del data_dict['objects']
            else:
                female = ["Female", "female"]
                age_range = ['12 or under', '12-15', '16-18']
                output = []
                for reg in data_dict['objects']:
                    if reg.data["key"] == "gender":
                        if reg.data["value"] in female:
                            output.append(reg.data["value"])
                    elif reg.data["key"] == "age":
                        if reg.data["value"] in age_range:
                            output.append(reg.data["value"])

                if len(output) == 2:
                    data_dict['U18'] = True
                else:
                    data_dict['U18'] = False

                del data_dict['objects']
        return data_dict


    def post_list(self, request, **kwargs):
        """
        Gets posted data so as to save it in the UserInteraction Table, but
        checks if the characters are not too long (if this is not done TastyPie
        returns a huge annoying error)
        """
        user_data = request.POST.dict()

        if (len(user_data['msisdn']) > 20):
            raise TastypieError("'msisdn' is longer than the maximum allowed length of 20")

        if len(user_data['feature']) > 30:
            raise TastypieError("'feature' is longer than the maximum allowed length of 30")

        if len(user_data['key']) > 100:
            raise TastypieError("'key' is longer than the maximum allowed length of 100")

        if len(user_data['value']) > 200:
            raise TastypieError("'value' is longer than the maximum allowed length of 200")

        if len(user_data['transport']) > 5:
            raise TastypieError("'transport' is longer than the maximum allowed length of 20")

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
