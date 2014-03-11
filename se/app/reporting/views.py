# Python library imports
from datetime import datetime
import re

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

def reporting(request):

    context = {'page': 'reporting'}
    context['total_users'] = len(User_Profile.objects.filter().all())
    user_profiles = User_Profile.objects.filter()
    users_complete = 0
    for user_profile in user_profiles:
        if len(str(user_profile.end_time)) > 0:
            users_complete += 1
    context['users_complete'] = users_complete 
    return render(request, 'objects/reporting.html', context)
