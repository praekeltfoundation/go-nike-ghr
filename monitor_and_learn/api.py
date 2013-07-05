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
        # dictionary. This function handles /api/mandl/
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])
            quizzes = []
            for quiz_i in range(len(data_dict['objects'])):
                quizzes.append(data_dict['objects'][quiz_i].data['id'])

            data_dict['quizzes'] = quizzes
            del (data_dict['objects'])
        return data_dict

    def alter_detail_data_to_serialize(self, request, data_dict):
        # Altering the response given by accessing different quiz IDs
        # This function handles /api/mandl/quiz_id/
        questions = {}  # Dict item to hold the questions structure
        quiz_ids = data_dict.data["quiz_ids"]  # Variable to hold the quiz dict
        first_question_id = []  # Variable to hold min id for start key
        last_question_id = []  # Variable to hold the max question id for menu endpoint

        for i in range(len(quiz_ids)):
            # Need to store end point for main_menu
            last_question_id.append(quiz_ids[i].data["id"])

        last_question_id = max(last_question_id)
        for question_i in range(len(quiz_ids)):
            # Looping through data and adding it to dict_item for final output
            q_id = "q_%s" % quiz_ids[question_i].data["id"]  # Variable for q_#
            questions[q_id] = {"choices": []}
            choices = []
            first_question_id.append(quiz_ids[question_i].data["id"])

            for answer_i in range(len(quiz_ids[question_i].data["quiz_ids"])):
                # For loop adds answer to a list that will be appended to dict.
                # also adds go to variables to the answer
                if quiz_ids[question_i].data["id"] == last_question_id:
                    next = "main_menu"
                else:
                    next = "q_%s" % (quiz_ids[question_i].data["id"] + 1)
                answer = quiz_ids[question_i].data["quiz_ids"][answer_i].data["answer"]
                choices.append([next, answer])

            questions[q_id] = {"question": quiz_ids[question_i].data["question"],
                               "choices": choices}

        first_question_id = min(first_question_id)
        data_dict.data["quiz"] = {"start": "q_%s" % first_question_id,
                                  "questions": questions}
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
