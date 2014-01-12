from django.shortcuts import render, render_to_response

from django.http import HttpRequest, HttpResponse

from generate_question import generate_question

from app.models import *

from django.contrib.auth import authenticate, login, logout
  
# Create your views here.

def landing(request):
    context = {'page': 'landing'}
    condition = request.GET['q']
    context['condition'] = condition
    request.session['condition'] = condition
    return render(request, "objects/landing.html", context)


def links(request):
    context = {'page': 'links'}
    if 'tick' in request.GET:
        if User.objects.filter(username=request.GET['tick']):
            context['error'] = 'A better way to handle returning users is coming.'
            return render(request, "objects/links.html", context)
        else:
            new_user = User.objects.create_user(username=request.GET['tick'], password='')
            new_user.save()
            user = authenticate(username=request.GET['tick'], password='')
            login(request, user)
            request.session['username'] = request.GET['tick']
            new_profile = User_Profile(user=new_user, tick=request.GET['tick'], ip_address=get_client_ip(request))
            new_profile.save()
            return render(request, "objects/links.html", context)

    else:
        context['error'] = 'Tick information is incorrect or absent.'
        return render(request, "objects/links.html", context)


def se(request):

    context = {'page': request.session['condition']}
    if request.user.is_authenticated():
        
        user_profile = User_Profile.objects.get(user=request.user)
        if 'qid' in request.GET:
            question = Question.objects.get(id=request.GET['qid'])
            context['question'] = question
            return render(request, 'objects/se.html', context)

        if not 'answered_index' in request.session:
            request.session['answered_index'] = 1
        
        if not 'answered_group' in request.session or request.session['answered_index'] <= 4:
            request.session['answered_group'] = 0
            question = Question.objects.get(id=request.session['answered_index'])
            request.session['answered_index'] = request.session['answered_index'] + 1 #Move both these to the function that submits the question's answer
            context['question'] = question
            return render(request, 'objects/se.html', context)

        elif request.session['answered_index'] > 4:
            request.session['answered_group'] = request.session['answered_group'] + 1 #Move both these to the function that submits the question's answer
            questions = Question.objects.filter(group=request.session['answered_group'])
            context['questions'] = questions
            return render(request, 'objects/select.html', context)

    else:
        return redirect('/')


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
