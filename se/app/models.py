from django.db import models

from django.contrib.auth.models import User

class Question(models.Model):

    LANGUAGE_CHOICES = (
        ('EN', 'English'),
        ('PO', 'Polish'),
        ('DE', 'German'),
        ('IT', 'Italian')
    )
    GROUP_CHOICES = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4')
    )
    english = models.CharField(max_length=500)
    italian = models.CharField(max_length=500)
    polish = models.CharField(max_length=500)
    german = models.CharField(max_length=500)
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)


class Answer(models.Model):

    text = models.CharField(max_length=150)
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)


class User_Profile(models.Model):

    EXPERIMENTAL_CONDITIONS = (
        ('TR', 'Traditional'),
        ('CO', 'Control'),
        ('AN', 'Anthropomorphic'),
        ('ST', 'Stationary'),
        ('IP', 'IP Tracking'),
        ('CL', 'User Click Tracking'),
        ('IN', 'Informal'),
        ('SI', 'Simple policy')
    )
    user = models.OneToOneField(User)
    ip_address = models.CharField(max_length=40)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=False, null=True)
    experimental_condition = models.CharField(max_length=2, choices=EXPERIMENTAL_CONDITIONS)
    privacy_clicked = models.BooleanField(default=False)
    questions_answered = models.ManyToManyField(Question)
    answers = models.ManyToManyField(Answer)
    tick = models.CharField(max_length=50)
    resolution = models.CharField(max_length=15)
