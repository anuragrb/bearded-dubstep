# Python library imports
import datetime
import re
import json
from time import *

# Django specific imports
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests
import logging

# App specific imports
from app.models import *

logger = logging.getLogger('custom.logger')

#the number of completes, terminates by question, over-quota terminates by question, incompletes, and progress towards sub-quota groups

def reporting(request):

    context = {'page': 'reporting'}
    context['total_users'] = len(User_Profile.objects.filter().all())
    user_profiles = User_Profile.objects.filter()
    questions = Question.objects.filter()
    answers = Answer.objects.filter()

    users_complete = 0

    now = datetime.datetime.utcnow()

    question_terminated = {}
    country_completes = {}
    country_incompletes = {}
    country_in_progress = {}

    for user_profile in user_profiles:

        time_start = user_profile.begin_time

        now = now.replace(tzinfo=None)
        time_start = time_start.replace(tzinfo=None)

        difference = now - time_start

        minutes = difference.seconds/60

        user_country = user_profile.country

        if minutes > 30:

            if str(user_profile.end_time) != 'None' or Answer.objects.filter(question_id=68).filter(user=user_profile.user):
                users_complete += 1
                if user_country in country_completes.iterkeys():
                    country_completes[user_country] += 1
                else:
                    country_completes[user_country] = 1

            else:
                user_answers = Answer.objects.filter(user=user_profile.user)
                user_answers = list(user_answers)
                if len(user_answers) > 0:
                    last_answer = user_answers[-1]
                    last_question = Question.objects.get(answer=last_answer)
                    qid = str(last_question.id)
                    if qid in question_terminated.iterkeys():
                        question_terminated[qid] += 1
                    else:
                        question_terminated[qid] = 1
                else:
                    if '1' in question_terminated.iterkeys():
                        question_terminated['1'] += 1
                    else:
                        question_terminated['1'] = 1
                if user_country in country_incompletes.iterkeys():
                    country_incompletes[user_country] += 1
                else:
                    if len(user_country) > 1:
                        country_incompletes[user_country] = 1
        else:
            if user_country in country_in_progress.iterkeys():
                country_in_progress[user_country] += 1
            else:
                country_in_progress[user_country] = 1

    context['country_in_progress'] = str(json.dumps(country_in_progress))
    context['country_completes'] = str(json.dumps(country_completes))
    context['country_incompletes'] = str(json.dumps(country_incompletes))
    context['question_terminated'] = str(json.dumps(question_terminated))
    context['users_complete'] = users_complete 
    return render(request, 'objects/reporting.html', context)
