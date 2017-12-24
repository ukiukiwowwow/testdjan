import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    def get_queryset(self):
        """
        Excludes any problems that aren't published yet.
        """
        return Student


class Password(models.Model):
    student_number = models.ForeignKey(Student, on_delete=models.CASCADE)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.password