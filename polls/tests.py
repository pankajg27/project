from asyncio import futures
from cgi import test

from urllib import response
from venv import create
from django.test import TestCase
import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse
# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_pulished_recently() reutrns False for questions whose pu_date
        is in the future.
        """
        time=timezone.now()+datetime.timedelta(days=30)
        future_question=Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns true for questions whose pub_date is within the lastday.
        """
        time=timezone.now()-datetime.timedelta(hours=23,minutes=59,seconds=59)
        recent_question=Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(),True)

def create_question(question_text,days):
    """Create a question with th e given 'question_text' and published the give number of
    'days' offset to now (negative ofr question published in the past,positive for question that yet to be published).
    """
    time=timezone.now() +datetime.timedelta(days=days) 
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionIndexviewTests(TestCase):
    def test_no_question(self):
        """
        if no questions exits,an appropriate message is displayed
        """
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])
    
    def test_past_question(self):
        """
        Question with a pub_date in the past are dispalyed on the index page
        """
        question=create_question(question_text="past question.",days=-30)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],[question],)
    
    def test_future_question(self):
        """
        Question with a pub_date in the future are't displayed on th index page.
        """
        create_question(question_text="Future question.",days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_question(self):
        """the question index page may dispaly mutiple questions.
        """
        question1 =create_question(question_text="Past question 1.",days=-30)
        question2 =create_question(question_text="past question 2.",days=-5)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],[question2, question1],
        )