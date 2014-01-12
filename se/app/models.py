from django.db import models

from django.contrib.auth.models import User

class Question(models.Model):

    LANGUAGE_CHOICES = (
        ('EN', 'English'),
        ('PO', 'Polish'),
        ('ES', 'Spanish'),
        ('IT', 'Italian')
    )
    language = models.CharField(max_length=15, choices=LANGUAGE_CHOICES)
    text = models.CharField(max_length=500)

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
    end_time = models.DateTimeField(auto_now_add=False)
    experimental_condition = models.CharField(max_length=2, choices=EXPERIMENTAL_CONDITIONS)
    privacy_clicked = models.BooleanField(default=False)
    questions_answered = models.ManyToManyField(Question)
    answers = models.ManyToManyField(Answer)
