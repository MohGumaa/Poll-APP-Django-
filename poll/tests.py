import datetime
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse

from .models import Question

c = Client()

def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and published the
    given number of 'days' offset to now (negative for questions published
    in the past, positive for questions that have yet to the published.)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently return False for questions whose pub_date in
        future.
        """
        future_question = create_question(question_text="future", days=30)
        self.assertIs(future_question.was_published_recently(), False)


    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently return True for question whose date
        is within the last day
        """
        recent_question = create_question(question_text="past", days=-1)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_question_create(self):
        q = create_question("Create new", 30)
        q.save()
        query = Question.objects.all()
        self.assertEqual(query.count(), 1)


class QuestionViewTests(TestCase):

    def test_no_question(self):
        """
        If no question exist, an message displayed.
        """
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No poll Available")
        # print(response.context['latest_question_list'])
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions within past date are displayed
        """
        create_question(question_text="past", days=-1)
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "past")
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: past>'])


    def test_future_question(self):
        """
        Questions within past date are displayed
        """
        create_question(question_text="future", days=10)
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No poll Available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Questions within past date are displayed
        """
        create_question(question_text="past", days=-1)
        create_question(question_text="future", days=10)
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "past")
        # print(response.context)
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: past>'])

    def test_two_past_question(self):
        """
        Questions within past date are displayed
        """
        create_question(question_text="past", days=-1)
        create_question(question_text="past1", days=-2)
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: past>', '<Question: past1>'])

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """ The quesiton with future data return 404 response"""
        future_question = create_question(question_text="future", days=10)
        res = c.get(f'detail/{future_question.id}')
        self.assertEqual(res.status_code, 404)

    def test_past_question(self):

        """ The quesiton with future data return 404 response"""
        past_question = create_question(question_text="past", days=-4)
        print(past_question.pub_date)
        res = c.get(reverse('poll:detail', args=(past_question.id,)))
        self.assertEqual(res.status_code, 200)
        # print(res.context)
        # self.assertIn(b'past',res.content)
        self.assertTrue(b'past'in res.content)
