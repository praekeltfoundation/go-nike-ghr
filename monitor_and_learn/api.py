from tastypie.resources import ModelResource
from tastypie import fields
from django.conf.urls import url
from monitor_and_learn.models import (MonitorAndLearningQuizId,
                               MonitorAndLearningQuizQuestion,
                               MonitorAndLearningQuizAnswer)


class MonitorAndLearningQuizIDResource(ModelResource):
    quiz_ids = fields.ToManyField('monitor_and_learn.api.MonitorAndLearningQuizQuestionResource',
                                 'quiz_ids', full=True)
    class Meta:
        # setting the resoucrce attributes
        resource_name = "mandl"
        allowed_methods = ['get']
        excludes = ['completed', 'active']
        include_resource_uri = False
        queryset = MonitorAndLearningQuizId.objects.all()

    def alter_list_data_to_serialize(self, request, data_dict):
        # Modifying the data to provide only what is needed in the right
        # form by removing the extra meta variables and editing the
        # dictionary
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])
            a = []
            for item in range(len(data_dict['objects'])):
                a.append(data_dict['objects'][item].data['id'])

            data_dict['quizzes'] = a
            del (data_dict['objects'])
        return data_dict

    def alter_detail_data_to_serialize(self, request, data_dict):
        # print data_dict
        # print len(data_dict)
        # print dir(data_dict.obj)
        print dir(data_dict.data["quiz_ids"])
        for item in range(len(data_dict.data["quiz_ids"])):
            print data_dict.data["quiz_ids"][item].data
        data_dict.data["start"] = "q1"

        del data_dict.data["quiz_ids"]
        del data_dict.data["id"]
        return data_dict

    # def dehydrate(self, bundle):
    #     print dir(self)
    #     print self.get_resource_uri(bundle_or_obj=bundle)
    #     bundle.data["apples"] = "Apples"
    #     del bundle.data["quiz_ids"]
    #     del bundle.data["id"]
    #     # print bundle.data
    #     # print dir(bundle)
    #     # print bundle.data["quiz_ids"][0].data
    #     # print bundle.data["id"]
    #     # print bundle.obj
    #     return bundle

    # def dispatch(self, request_type, request, **kwargs):
    #     print dir(self)
    # def prepend_urls(self):
    #     return[
    #         url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/" %
    #             (self._meta.resource_name), self.wrap_view('filter_questions'),
    #             name="filter_questions")
    #     ]

    # def filter_questions(self, request, **kwargs):
    #     print dir(self)
    #     queryset = MonitorAndLearningQuizId.objects.all()
    #     print queryset
    #     print self.build_bundle()
    #     object_list = {"apples": 1}
    #     return self.create_response(request, object_list)


class MonitorAndLearningQuizQuestionResource(ModelResource):
    quiz_ids = fields.ToManyField('monitor_and_learn.api.MonitorAndLearningQuizAnswerResource',
                                  'question_ids', full=True)

    class Meta:
        excludes = []
        include_resource_uri = False
        queryset = MonitorAndLearningQuizQuestion.objects.all()


class MonitorAndLearningQuizAnswerResource(ModelResource):
    class Meta:
        queryset = MonitorAndLearningQuizAnswer.objects.all()
