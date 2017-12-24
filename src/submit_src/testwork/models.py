
import datetime
from django.db import models
from django.utils import timezone

from django import forms


# Create your models here.
class Problem(models.Model):
    title = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')
    def was_published_recently(self):
        now=timezone.now()
        return now- datetime.timedelta(days=1) <= self.pub_date <= now
    def __str__(self):
        return self.title
    @classmethod
    def create(cls, title):
        problem = cls(title=title)
        # whatk
        return problem

class Choice(models.Model):
    detail = models.ForeignKey(Problem, on_delete=models.CASCADE)
    detail_text = models.CharField(max_length=200)
    votes = models.BooleanField(default=False)
    def __str__(self):
        return self.detail_text
        
class Answer(models.Model):
    ans= models.ForeignKey(Problem, on_delete=models.CASCADE)
    ans_text = models.CharField(max_length=200)
    def __str__(self):
        return self.ans_text

