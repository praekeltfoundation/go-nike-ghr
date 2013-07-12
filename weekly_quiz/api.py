from tastypie.resources import ModelResource
from tastypie import fields
from weekly_quiz.models import (WeeklyQuizId,
                                WeeklyQuizQuestion,
                                WeeklyQuizAnswer)


class WeeklyQuizIDResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    path = 'weekly_quiz.api.WeeklyQuizQuestionResource'
    wq_quiz_id = fields.ToManyField(path,
                                    'wq_quiz_id', full=True)

    class Meta:
        # setting the resoucrce attributes
        resource_name = "weeklyquiz"
        allowed_methods = ['get']
        excludes = ['completed', 'active']
        include_resource_uri = False
        queryset = WeeklyQuizId.objects.all()

    def get_object_list(self, request):
        """
        Filters the queryset in meta to get the specific Article required
        ordered by the primary key descending.
        """
        query = super(WeeklyQuizIDResource, self).get_object_list(request)
        return query.filter(active=True).order_by('-pk')

    def alter_list_data_to_serialize(self, request, data_dict):
        """
        Modifying the data to provide the quiz and answers and responses.
        Structure is {quiz:{start:"q_id", quiz_details: {answers:{}, questions: {}}}}
        This function handles /api/weeklyquiz/
        """
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])

            if data_dict["objects"] != []:
                wq_data = data_dict["objects"][0].data["wq_quiz_id"]
                questions = {}  # Dict item to hold final question structure
                answers = {}  # Dict item to hold final answer structure
                first_question_id = []  # Variable to hold min id for start key
                last_question_id = []  # Variable to hold the max question id for menu endpoint

                # Variable to hold the max question id for menu endpoint
                question_ids = [bundle.data["id"] for bundle in wq_data]
                first_question_id = min(question_ids)
                last_question_id = max(question_ids)

                # Looping through data and adding it to questions dict for final output
                for question_bundle in wq_data:
                    q_id = "q_%s" % question_bundle.data["id"]

                    choices = []  # List to hold the final answer and the "next q_id"

                    # Looping through data and adding to choices list for final output
                    # Also adds the "next question"
                    # Loop also adds data to answers{}
                    for answer_bundle in question_bundle.data["wq_question_id"]:
                        a_id = answer_bundle.data["id"]
                        answer = answer_bundle.data["answer"]
                        q_id_a_id = "%s_a_%s" % (q_id, a_id)
                        response = answer_bundle.data["response"]
                        choices.append([q_id_a_id, answer])

                        if question_bundle.data["id"] == last_question_id:
                            next = "main_menu"
                        else:
                            next = "q_%s" % (question_bundle.data["id"] + 1)

                        answers[q_id_a_id] = {"response": response, "next": next}

                    questions[q_id] = {"question": question_bundle.data["question"],
                                       "choices": choices}

                data_dict['quiz'] = {"start": "q_%s" % first_question_id,
                                     "quiz_details": {"questions": questions,
                                                      "answers": answers}}
            del (data_dict['objects'])
        return data_dict


class WeeklyQuizQuestionResource(ModelResource):
    """
    Class that returns the Questions to QuizIDResource based on Foreign Key Assoication
    """
    path = 'weekly_quiz.api.WeeklyQuizAnswerResource'
    wq_question_id = fields.ToManyField(path,
                                        'wq_question_id', full=True)

    class Meta:
        include_resource_uri = False
        queryset = WeeklyQuizQuestion.objects.all()


class WeeklyQuizAnswerResource(ModelResource):
    """
    Class that returns the Answers to QuestionResource based on Foreign Key Assoication
    """
    class Meta:
        queryset = WeeklyQuizAnswer.objects.all()
