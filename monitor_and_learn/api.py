from tastypie.resources import ModelResource
from tastypie import fields
from monitor_and_learn.models import (MonitorAndLearningQuizId,
                               MonitorAndLearningQuizQuestion,
                               MonitorAndLearningQuizAnswer)


class MonitorAndLearningQuizIDResource(ModelResource):
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


class MonitorAndLearningQuizQuestionResource(ModelResource):

    quiz_id = fields.ForeignKey('MonitorAndLearningQuizIDResource',
                                'quiz_id',
                                full=True)

    class Meta:
        queryset = MonitorAndLearningQuizQuestion.objects.all()
        excludes = []
        include_resource_uri = False
