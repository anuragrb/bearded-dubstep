from django.db import models

from django.contrib.auth.models import User


class Option(models.Model):

    english = models.CharField(max_length=500)
    italian = models.CharField(max_length=500)
    polish = models.CharField(max_length=500)
    german = models.CharField(max_length=500)


class Question(models.Model):

    english = models.CharField(max_length=500)
    italian = models.CharField(max_length=500)
    polish = models.CharField(max_length=500)
    german = models.CharField(max_length=500)
    group = models.CharField(max_length=2)
    options = models.ManyToManyField(Option)
    category = models.CharField(max_length=2)


class Answer(models.Model):

    text = models.CharField(max_length=10000)
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    time_posted = models.DateTimeField(auto_now_add=True)
    clicktime = models.CharField(max_length=10, null=True)


class Search_Query(models.Model):

    text = models.CharField(max_length=10000)
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    time_posted = models.DateTimeField(auto_now_add=True)


class Search_Result(models.Model):

    text = models.CharField(max_length=1000)
    href = models.CharField(max_length=1000)
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    time_posted = models.DateTimeField(auto_now_add=True)


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
    city = models.CharField(max_length=100)
    browser = models.CharField(max_length=100)
    entrance_time = models.DateTimeField(auto_now_add=True)
    begin_time = models.DateTimeField(auto_now_add=False, null=True)
    end_time = models.DateTimeField(auto_now_add=False, null=True)
    experimental_condition = models.CharField(max_length=2, choices=EXPERIMENTAL_CONDITIONS)
    privacy_clicked = models.IntegerField()
    questions_answered = models.ManyToManyField(Question)
    answers = models.ManyToManyField(Answer)
    tick = models.CharField(max_length=50)
    screen_resolution = models.CharField(max_length=15)
    browser_resolution = models.CharField(max_length=15)
    search_queries = models.ManyToManyField(Search_Query)
    results_clicked = models.ManyToManyField(Search_Result)
    hasflash = models.CharField(max_length=10)
    mturk_payment_code = models.CharField(max_length=10)
    country = models.CharField(max_length=25)
