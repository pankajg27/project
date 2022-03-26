import datetime
import imp
from pydoc import describe
from xmlrpc.client import boolean
from django.contrib import admin

from django.db import models
from django.utils import timezone

# Create you models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
         return self.question_text
    def was_published_recently(self):
        now= timezone.now()
        return now -datetime.timedelta(days=1)<=self.pub_date<=now
   
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='published reacentlty ?',
    ) 
    def was_published_recently(self):
        now=timezone.now()
        return now -datetime.timedelta(days=1)<=self.pub_date<=now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
        