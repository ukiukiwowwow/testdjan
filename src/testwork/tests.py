import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import *

# Create your tests here.
class problemModelTests(TestCase):

    def test_was_published_recently_with_future_problem(self):
        """
        was_published_recently() returns False for problems whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_problem = Problem(pub_date=time)
        self.assertIs(future_problem.was_published_recently(), False)
    def test_was_published_recently_with_old_problem(self):
        """
        was_published_recently() returns False for problems whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_problem = Problem(pub_date=time)
        self.assertIs(old_problem.was_published_recently(), False)

    def test_was_published_recently_with_recent_problem(self):
        """
        was_published_recently() returns True for problems whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_problem = Problem(pub_date=time)
        self.assertIs(recent_problem.was_published_recently(), True)


def create_problem(problem_text, days):
    """
    Create a problem with the given `problem_text` and published the
    given number of `days` offset to now (negative for problems published
    in the past, positive for problems that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Problem.objects.create(title=problem_text, pub_date=time)

class ProblemIndexViewTests(TestCase):
    def test_no_problems(self):
        """
        If no problems exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('testwork:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No testwork are available.")
        self.assertQuerysetEqual(response.context['latest_problem_list'], [])

    def test_past_problem(self):
        """
        Problems with a pub_date in the past are displayed on the
        index page.
        """
        create_problem(problem_text="Past problem.", days=-30)
        response = self.client.get(reverse('testwork:index'))
        self.assertQuerysetEqual(
            response.context['latest_problem_list'],
            ['<Problem: Past problem.>']
        )

    def test_future_problem(self):
        """
        Problems with a pub_date in the future aren't displayed on
        the index page.
        """
        create_problem(problem_text="Future problem.", days=30)
        response = self.client.get(reverse('testwork:index'))
        self.assertContains(response, "No testwork are available.")
        self.assertQuerysetEqual(response.context['latest_problem_list'], [])

    def test_future_problem_and_past_problem(self):
        """
        Even if both past and future problems exist, only past problems
        are displayed.
        """
        create_problem(problem_text="Past problem.", days=-30)
        create_problem(problem_text="Future problem.", days=30)
        response = self.client.get(reverse('testwork:index'))
        self.assertQuerysetEqual(
            response.context['latest_problem_list'],
            ['<Problem: Past problem.>']
        )

    def test_two_past_problems(self):
        """
        The problems index page may display multiple problems.
        """
        create_problem(problem_text="Past problem 1.", days=-30)
        create_problem(problem_text="Past problem 2.", days=-5)
        response = self.client.get(reverse('testwork:index'))
        self.assertQuerysetEqual(
            response.context['latest_problem_list'],
            ['<Problem: Past problem 2.>', '<Problem: Past problem 1.>']
        )
class ProblemDetailViewTests(TestCase):
    def test_future_problem(self):
        """
        The detail view of a problem with a pub_date in the future
        returns a 404 not found.
        """
        future_problem = create_problem(problem_text='Future problem.', days=5)
        url = reverse('testwork:detail', args=(future_problem.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_problem(self):
        """
        The detail view of a problem with a pub_date in the past
        displays the problem's text.
        """
        past_problem = create_problem(problem_text='Past Problem.', days=-5)
        url = reverse('testwork:detail', args=(past_problem.id,))
        response = self.client.get(url)
        self.assertContains(response, past_problem.title)