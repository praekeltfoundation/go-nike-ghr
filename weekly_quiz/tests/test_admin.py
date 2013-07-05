from django.test import TestCase
from weekly_quiz.admin import (WeeklyQuizIdAdmin, WeeklyQuizQuestionAdmin)


class TestQuizIdAdmin(TestCase):
    def test_admin_quiz_id_works(self):
        data = {"active": False, "name": "Quiz 1"}
        wqid = WeeklyQuizIdAdmin.form(data=data)
        self.assertEqual(wqid.data["name"], 'Quiz 1')
        self.assertEqual(wqid.data["active"], False)

    def test_admin_quiz_id_no_name(self):
        data = {"active": False}
        wqid = WeeklyQuizIdAdmin.form(data=data)
        # print dir(wqid)
        self.assertIn(["This field is required."], wqid.errors.values())

    def test_admin_quiz_id_active(self):
        data = {"active": True, "name": "Quiz 1"}
        wqid = WeeklyQuizIdAdmin.form(data=data)
        self.assertIn(["This quiz has less than 3 questions, finish"
                      " questions to activate"], wqid.errors.values())
