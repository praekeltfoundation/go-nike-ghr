from tastypie.resources import ModelResource
from tastypie import fields
from opinions.models import (Opinion,
                             OpinionPollId,
                             OpinionPollOpinion,
                             OpinionPollChoices)
import copy


class OpinionResource(ModelResource):
    class Meta:
        # Setting the api meta attributes
        resource_name = "opinions/sms"
        allowed_methods = ['get']
        excludes = ['updated_at', 'id']
        include_resource_uri = False

        queryset = Opinion.objects.all()

    def alter_list_data_to_serialize(self, request, data_dict):
        # Modifying the data to provide only what is needed in the right
        # form by removing the extra meta variables and editing the
        # dictionary
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])

            data_dict['opinions'] = (copy.copy(data_dict['objects'][0]))
            del (data_dict['objects'])
        return data_dict


class OpinionPollIdResource(ModelResource):
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
        query = super(OpinionPollIdResource, self).get_object_list(request)
        query = (query.filter(active=True))
        return query

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])
            if data_dict["objects"] == []:
                data_dict['quiz'] = False
                del (data_dict['objects'])

            else:
                opinions = {}
                # print data_dict['objects'][1].data["opinionpollid"][0].data
                print data_dict['objects'][1].data["opinionpollid"]
                # print [k for k in data_dict['objects'][1].data.iterkeys()]
                for op_id_i in range(len(data_dict['objects'])):
                    opinion_view_dict = {}
                    op_view_data = data_dict['objects'][op_id_i]
                    opinion_view_id = "opinion_view_%s" % op_view_data.data["id"]

                    op_opinions = op_view_data.data["opinionpollid"]

                    opinion_opinions_dict = {}
                    for op_op_i in range(len(op_opinions)):
                        o_id = "o_%s" % op_opinions[op_op_i].data["id"]
                        opinion_actual = op_opinions[op_op_i].data["opinion"]

                        choices = []


                        opinion_opinions_dict[o_id] = {"opinions": opinion_actual,
                                                        "choices": choices}

                    opinion_view_dict["start"] = ""
                    opinion_view_dict["views"] = opinion_opinions_dict
                    opinions[opinion_view_id] = opinion_view_dict

                data_dict['opinions'] = opinions
                del (data_dict['objects'])
        return data_dict


class OpinionPollOpinionResource(ModelResource):
    path = 'opinions.api.OpinionPollChoicesResource'
    opinionpollopinion = fields.ToManyField(path,
                                            'opinionpollopinion',
                                            full=True)

    class Meta:
        queryset = OpinionPollOpinion.objects.all()
        include_resource_uri = False


class OpinionPollChoicesResource(ModelResource):
    class Meta:
        queryset = OpinionPollChoices.objects.all()
        include_resource_uri = False
