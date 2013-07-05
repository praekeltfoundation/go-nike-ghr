from tastypie.resources import ModelResource
from tastypie import fields
from weekly_quiz.models import (WeeklyQuizId,
                                WeeklyQuizQuestion,
                                WeeklyQuizAnswer)


class WeeklyQuizIDResource(ModelResource):
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
        # Filters the queryset in meta to get the specific Article required
        query = super(WeeklyQuizIDResource, self).get_object_list(request)
        query = (query.order_by('-pk'))

        return query

    def alter_list_data_to_serialize(self, request, data_dict):
        # Modifying the data to provide only what is needed in the right
        # form by removing the extra meta variables and editing the
        # dictionary. This function handles /api/mandl/
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])

            if data_dict["objects"] == []:
                data_dict['quiz'] = False
                del (data_dict['objects'])

            else:
                wq_data = data_dict["objects"][0].data["wq_quiz_id"]
                questions = {}  # Dict item to hold final question structure
                answers = {}  # Dict item to hold final answer structure
                first_question_id = []  # Variable to hold min id for start key
                last_question_id = []  # Variable to hold the max question id for menu endpoint

                # Variable to hold the max question id for menu endpoint
                last_question_id = max([wq_data[i].data["id"] for i in range(len(wq_data))])

                for question_i in range(len(wq_data)):
                    q_id = "q_%s" % wq_data[question_i].data["id"]

                    # dict_item_question[q_id] = {"answers": []}
                    choices = []
                    first_question_id.append(wq_data[question_i].data["id"])

                    for answer_i in range(len(wq_data[question_i].data["wq_question_id"])):
                        a_id = wq_data[question_i].data["wq_question_id"][answer_i].data["id"]
                        answer = wq_data[question_i].data["wq_question_id"][answer_i].data["answer"]
                        q_id_a_id = "%s_a_%s" % (q_id, a_id)
                        response = wq_data[question_i].data["wq_question_id"][answer_i].data["response"]
                        choices.append([q_id_a_id, answer])

                        if wq_data[question_i].data["id"] == last_question_id:
                            next = "main_menu"
                        else:
                            next = "q_%s" % (wq_data[question_i].data["id"] + 1)

                        answers[q_id_a_id] = {"response": response, "next": next}

                    questions[q_id] = {"question": wq_data[question_i].data["question"],
                                       "choices": choices}
                first_question_id = min(first_question_id)
                data_dict['quiz'] = {"start": "q_%s" % first_question_id,
                                     "quiz_details": {"questions": questions,
                                                      "answers": answers}}
                del (data_dict['objects'])
        return data_dict


class WeeklyQuizQuestionResource(ModelResource):
    path = 'weekly_quiz.api.WeeklyQuizAnswerResource'
    wq_question_id = fields.ToManyField(path,
                                        'wq_question_id', full=True)

    class Meta:
        excludes = []
        include_resource_uri = False
        queryset = WeeklyQuizQuestion.objects.all()


class WeeklyQuizAnswerResource(ModelResource):
    class Meta:
        queryset = WeeklyQuizAnswer.objects.all()
