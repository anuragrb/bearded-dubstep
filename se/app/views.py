from django.shortcuts import render

from django.http import HttpRequest  

from generate_question import generate_question

from app.models import *

from django.contrib.auth import authenticate, login, logout
  
# Create your views here.

def landing(request):
    context = {'page': 'landing'}
    condition = request.GET['q']

    context['condition'] = condition
    return render(request, "objects/landing.html", context)


def links(request):
    context = {'page': 'links'}
    if 'tick' in request.GET:
        if User.objects.filter(username=request.GET['tick']):
            context['error'] = 'A user with this tick has already taken this survey.'
        else:
            new_user = User.objects.create_user(username=request.GET['tick'], password='')
            new_user.save()
            user = authenticate(username=request.GET['tick'], password='')
            login(request, user)
            new_profile = User_Profile(user=new_user, tick=request.GET['tick'], ip_address=get_client_ip(request))
            new_profile.save()
    return render(request, "objects/links.html", context)


def se(request):
    context = {'page': request.GET['page']}
    if 'index' in request.GET:
        index = request.GET['index']
    if 'language' in request.GET:
        language = request.GET['language']
    context['index'] = index
    if 'question' in request.GET:
        context['question'] = request.GET['question']
        return render(request, 'objects/se.html', context)
    question = generate_question(index)
    context['question'] = question
    context['client_address'] = get_client_ip(request)
    if question == 'Done':
        return render(request, 'objects/questionnaire.html', context)
    if type(question) == list:
        return render(request, 'objects/select.html', context)
    else:    
        return render(request, "objects/se.html", context)


def privacy(request):
    context = {'page': 'privacy'}
    return render(request, "objects/privacy.html")


def privacy_simplified(request):
    context = {'page': 'privacy'}
    return render(request, "objects/privacy.html")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
