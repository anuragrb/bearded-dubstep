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

    return render(request, 'objects/reporting.html')