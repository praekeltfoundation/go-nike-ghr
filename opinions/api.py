from tastypie.resources import ModelResource
from tastypie import fields
from opinions.models import (Opinion,
                             OpinionPollId,
                             OpinionPollOpinion,
                             OpinionPollChoices)
import copy


class OpinionResource(ModelResource):
    """
    This resource handles /api/opinions/sms/
    """
    class Meta:
        # Setting the api meta attributes
        resource_name = "opinions/sms"
        allowed_methods = ['get']
        excludes = ['updated_at', 'id']
        include_resource_uri = False

        queryset = Opinion.objects.all()

    def alter_list_data_to_serialize(self, request, data_dict):
        """
        Modifying the data to provide only what is needed in the right
        form by removing the extra meta variables and editing the
        dictionary
        """
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])

            data_dict['opinions'] = (copy.copy(data_dict['objects'][0]))
            del data_dict['objects']
        return data_dict


class OpinionPollIdResource(ModelResource):
    """
    This resource handles /api/opinions/view/
    """
    path = 'opinions.api.OpinionPollOpinionResource'
    opinionpollid = fields.ToManyField(path,
                                       'opinionpollid',
                                       full=True)

    class Meta:
        resource_name = "opinions/view"
        allowed_methods = ['get']
        excludes = ['active']
        include_resource_uri = False

        queryset = OpinionPollId.objects.all()

    def get_object_list(self, request):
        """
        tastypie function that returns filtered data
        """
        query = super(OpinionPollIdResource, self).get_object_list(request)
        return query.filter(active=True)

    def alter_list_data_to_serialize(self, request, data_dict):
        """
        overiding tastypie function that returns data in required format
        """
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del data_dict['meta']
            if data_dict["objects"] == []:
                data_dict['quiz'] = False
                del data_dict['objects']

            else:
                opinions = {}
                for op_view_data in data_dict['objects']:
                    opinion_view_dict = {}
                    opinion_view_id = "opinion_view_%s" % (
                        op_view_data.data["id"],)
                    op_opinions = op_view_data.data["opinionpollid"]

                    op_opinion_ids = [bundle.data["id"]
                                      for bundle in op_opinions]
                    start_opinion_id = min(op_opinion_ids)
                    exit_opinion_id = max(op_opinion_ids)

                    opinion_opinions_dict = {}
                    for op_opinion in op_opinions:
                        o_id = "o_%s" % op_opinion.data["id"]
                        opinion_actual = op_opinion.data["opinion"]

                        choices = []
                        op_choices = op_opinion.data["opinionpollopinion"]
                        for op_choice in op_choices:
                            if op_opinion.data["id"] == exit_opinion_id:
                                next = "main_menu"
                            else:
                                next = "o_%s" % (op_opinion.data["id"] + 1,)

                            choice_actual = op_choice.data["choices"]
                            choices.append([next, choice_actual])

                        opinion_opinions_dict[o_id] = {
                            "opinions": opinion_actual,
                            "choices": choices,
                        }

                    opinion_view_dict["start"] = 'o_%s' % start_opinion_id
                    opinion_view_dict["views"] = opinion_opinions_dict
                    opinions[opinion_view_id] = opinion_view_dict

                data_dict['opinions'] = opinions
                del data_dict['objects']
        return data_dict


class OpinionPollOpinionResource(ModelResource):
    """
    Class that returns the different opinions to opinion id.
    Has many OpinionPollChoicesResource but belongs to
    OpinionPollIdResource
    """
    path = 'opinions.api.OpinionPollChoicesResource'
    opinionpollopinion = fields.ToManyField(path,
                                            'opinionpollopinion',
                                            full=True)

    class Meta:
        queryset = OpinionPollOpinion.objects.all()
        include_resource_uri = False


class OpinionPollChoicesResource(ModelResource):
    """
    Class that returns the choices, belongs to OpinionPollOpinionResource
    """
    class Meta:
        queryset = OpinionPollChoices.objects.all()
        include_resource_uri = False
