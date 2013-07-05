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
                min_id = []  # Variable to hold min id for start key
                max_id = []  # Variable to hold the max question id for menu endpoint
                for i in range(len(wq_data)):
                    max_id.append(wq_data[i].data["id"])
                max_id = max(max_id)

                for i in range(len(wq_data)):
                    q_id = "q_%s" % wq_data[i].data["id"]

                    # dict_item_question[q_id] = {"answers": []}
                    x = []
                    min_id.append(wq_data[i].data["id"])

                    for j in range(len(wq_data[i].data["wq_question_id"])):
                        k = wq_data[i].data["wq_question_id"][j].data["id"]
                        l = wq_data[i].data["wq_question_id"][j].data["answer"]
                        m = "%s_a_%s" % (q_id, k)
                        n = wq_data[i].data["wq_question_id"][j].data["response"]
                        x.append([m, l])

                        if wq_data[i].data["id"] == max_id:
                            next = "main_menu"
                        else:
                            next = "q_%s" % (wq_data[i].data["id"] + 1)

                        answers[m] = {"response": n, "next": next}

                    questions[q_id] = {"question": wq_data[i].data["question"],
                                       "choices": x}
                min_id = min(min_id)
                data_dict['quiz'] = {"start": "q_%s" % min_id,
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
