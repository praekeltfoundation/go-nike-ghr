# from django.test import TestCase
# from weekly_quiz.admin import (WeeklyQuizIdAdmin, WeeklyQuizQuestionAdmin)
# from weekly_quiz.models import (WeeklyQuizQuestion)
# from django.contrib.admin.sites import AdminSite


# class TestQuizIdAdmin(TestCase):
#     def test_admin_quiz_id_works(self):
#         # print dir(WeeklyQuizIdAdmin)
#         data = {"active": False, "name": "Quiz 1"}
#         wqid = WeeklyQuizIdAdmin.form(data=data)
#         self.assertEqual(wqid.data["name"], 'Quiz 1')
#         self.assertEqual(wqid.data["active"], False)

#     def test_admin_quiz_id_no_name(self):
#         # print dir(WeeklyQuizIdAdmin)
#         data = {"active": False,}
#         wqid = WeeklyQuizIdAdmin.form(data=data)
#         # print dir(wqid)
#         self.assertIn(["This field is required."], wqid.errors.values())

#     def test_admin_quiz_id_active(self):
#         # print dir(WeeklyQuizIdAdmin)
#         data = {"active": True, "name": "Quiz 1"}
#         wqid = WeeklyQuizIdAdmin.form(data=data)
#         self.assertIn(["This quiz has less than 3 questions, finish"
#                       " questions to activate"], wqid.errors.values())


# class TestQuizQuestionAdmin(TestCase):
#     def test_admin_question_works(self):
#         # print dir(WeeklyQuizQuestionAdmin)
#         wqid = WeeklyQuizQuestionAdmin(WeeklyQuizQuestion, AdminSite())
#         wqid_form = wqid.get_formsets(None)
#         print dir(wqid_form)
#         print list(wqid_form)
