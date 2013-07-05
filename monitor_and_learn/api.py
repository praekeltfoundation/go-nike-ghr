from tastypie.resources import ModelResource
from tastypie import fields
from monitor_and_learn.models import (MonitorAndLearningQuizId,
                                      MonitorAndLearningQuizQuestion,
                                      MonitorAndLearningQuizAnswer)


class MonitorAndLearningQuizIDResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    path = 'monitor_and_learn.api.MonitorAndLearningQuizQuestionResource'
    quiz_ids = fields.ToManyField(path,
                                  'quiz_ids', full=True)

    class Meta:
        resource_name = "mandl"
        allowed_methods = ['get']
        excludes = ['completed', 'active']
        include_resource_uri = False
        queryset = MonitorAndLearningQuizId.objects.all()

    def alter_list_data_to_serialize(self, request, data_dict):
        """
        Modifying the data to provide only the quiz id and nothing else.
        This function handles /api/mandl/
        """
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])
            quizzes = []  # List to hold the quiz IDs
            for quiz_i in range(len(data_dict['objects'])):
                quizzes.append(data_dict['objects'][quiz_i].data['id'])

            data_dict['quizzes'] = quizzes  # Adding the quiz ids to quizzes
            del (data_dict['objects'])
        return data_dict

    def alter_detail_data_to_serialize(self, request, data_dict):
        """
        Modifying the data for the individual quiz to return data in
        the required structure. This function handles /api/mandl/#/
        """
        questions = {}  # Dict item to hold the questions structure
        quiz_ids = data_dict.data["quiz_ids"]  # Variable to hold the quiz dict
        first_question_id = []  # Variable to hold min id for start key

        # Variable to hold the max question id for menu endpoint
        last_question_id = max([quiz_ids[i].data["id"] for i in range(len(quiz_ids))])

        # Looping through data and adding it to questions dict for final output
        for question_i in range(len(quiz_ids)):
            q_id = "q_%s" % quiz_ids[question_i].data["id"]  # Variable for q_#
            choices = []  # List to hold the final answer and "next"
            first_question_id.append(quiz_ids[question_i].data["id"])

            # Looping through data and adding to choices list for final output
            # Also adds the "next question" to go to
            for answer_i in range(len(quiz_ids[question_i].data["quiz_ids"])):
                if quiz_ids[question_i].data["id"] == last_question_id:
                    next = "main_menu"
                else:
                    next = "q_%s" % (quiz_ids[question_i].data["id"] + 1)

                answer = (quiz_ids[question_i].
                          data["quiz_ids"][answer_i].data["answer"])
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
    """
    Class that returns the Questions to QuizIDResource based on
    Foreign Key Assoication
    """

    path = 'monitor_and_learn.api.MonitorAndLearningQuizAnswerResource'
    quiz_ids = fields.ToManyField(path,
                                  'question_ids', full=True)

    class Meta:
        include_resource_uri = False
        queryset = MonitorAndLearningQuizQuestion.objects.all()


class MonitorAndLearningQuizAnswerResource(ModelResource):
    """
    Class that returns the Answers to QuestionResource based on Foreign
    Key Assoication
    """
    class Meta:
        queryset = MonitorAndLearningQuizAnswer.objects.all()
