from tastypie.resources import ModelResource
from tastypie import fields
from monitor_and_learn.models import (MonitorAndLearningQuizId,
                               MonitorAndLearningQuizQuestion,
                               MonitorAndLearningQuizAnswer)


class MonitorAndLearningQuizIDResource(ModelResource):
    path = 'monitor_and_learn.api.MonitorAndLearningQuizQuestionResource'
    quiz_ids = fields.ToManyField(path,
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
        # Altering the response given by accessing different quiz IDs
        dict_item = {}  # Dict item to hold final structure
        quiz_ids = data_dict.data["quiz_ids"]
        min_id = []  # Variable to hold min id for start key
        max_id = []  # Variable to hold the max question id for menu endpoint

        for i in range(len(quiz_ids)):
            max_id.append(quiz_ids[i].data["id"])

        max_id = max(max_id)
        for i in range(len(quiz_ids)):
            q_id = "q_%s" % quiz_ids[i].data["id"]
            dict_item[q_id] = {"choices": []}
            x = []
            min_id.append(quiz_ids[i].data["id"])

            for j in range(len(quiz_ids[i].data["quiz_ids"])):
                if quiz_ids[i].data["id"] == max_id:
                    y = "main_menu"
                else:
                    y = "q_%s" % (quiz_ids[i].data["id"] + 1)
                z = quiz_ids[i].data["quiz_ids"][j].data["answer"]
                x.append([y, z])

            dict_item[q_id] = {"question": quiz_ids[i].data["question"],
                               "choices": x}
        min_id = min(min_id)
        data_dict.data["quiz"] = {"start": "q_%s" % min_id,
                                  "questions": dict_item}
        del data_dict.data["quiz_ids"]
        del data_dict.data["id"]
        return data_dict


class MonitorAndLearningQuizQuestionResource(ModelResource):
    path = 'monitor_and_learn.api.MonitorAndLearningQuizAnswerResource'
    quiz_ids = fields.ToManyField(path,
                                  'question_ids', full=True)

    class Meta:
        excludes = []
        include_resource_uri = False
        queryset = MonitorAndLearningQuizQuestion.objects.all()


class MonitorAndLearningQuizAnswerResource(ModelResource):
    class Meta:
        queryset = MonitorAndLearningQuizAnswer.objects.all()
