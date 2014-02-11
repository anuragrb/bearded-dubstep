from django.shortcuts import render, render_to_response, redirect

from django.http import HttpRequest, HttpResponse

from generate_question import generate_question

from datetime import datetime

import re

from app.models import *

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

import requests
  
# Create your views here.

def landing(request):
    context = {'page': 'landing'}
    if request.user.is_authenticated():

        EXPERIMENTAL_CONDITIONS = {
            'TR': 'se_traditional',
            'CO': 'se_control',
            'AN': 'se_anthropomorphic',
            'ST': 'se_static',
            'IP': 'se_ip',
            'CL': 'se_tracking',
            'IN': 'se_informal',
            'SI': 'se_simplified'
        }
        conditions = dict((EXPERIMENTAL_CONDITIONS[k], k) for k in EXPERIMENTAL_CONDITIONS)
        user_profile = User_Profile.objects.get(user=request.user)
        if 'q' in request.GET:
            condition = request.GET['q']
        else:
            return redirect('/')
        context['condition'] = condition
        request.session['condition'] = condition
        if not 'language' in request.session:
            request.session['language'] = True
            request.session['language'] = 'EN'
        try:
            user_profile.experimental_condition = conditions[condition]
        except Exception as e:
            context['error'] = 'Malformed input parameter'
            return redirect('/')
        user_profile.screen_resolution = request.session['screen_resolution']
        user_profile.browser_resolution = request.session['browser_resolution']
        user_profile.browser = request.session['browser']
        user_profile.save()
        return render(request, "objects/landing.html", context)
    else:
        return redirect('/')


def links(request):
    context = {'page': 'links'}
    if request.is_ajax:
        if not 'screenresolution' in request.POST:
            pass
        else:
            screen_resolution = request.POST['screenresolution']
            browser_resolution = request.POST['browserresolution']
            browser = request.POST['browser']
            request.session['screen_resolution'] = screen_resolution
            request.session['browser_resolution'] = browser_resolution
            request.session['browser'] = browser

    if 'tick' in request.GET:

        if User.objects.filter(username=request.GET['tick']):

            if request.user.is_authenticated():
                return redirect('/se')
            else:
                user = authenticate(username=request.GET['tick'], password='')
                login(request, user)
                return redirect('/se')
            #context['error'] = 'A better way to handle returning users is coming.'
            #return render(request, "objects/links.html", context)
        else:

            new_user = User.objects.create_user(username=request.GET['tick'], password='')
            new_user.save()
            user = authenticate(username=request.GET['tick'], password='')
            login(request, user)
            request.session['username'] = request.GET['tick']
            try:
                r = requests.get('http://freegeoip.net/csv/' + get_client_ip(request))
                city = r.text.split(',')[5]
                city = city[1:-1]
                if len(city) < 1:
                    request.session['city'] = ''
                else:
                    request.session['city'] = city
            except Exception as e:
                request.session['city'] = ''
            new_profile = User_Profile(user=new_user, tick=request.GET['tick'], ip_address=get_client_ip(request), privacy_clicked=0, city=city)
            request.session['privacy_clicked'] = 0
            new_profile.save()
            return render(request, "objects/links.html", context)

    else:
        if request.user.is_authenticated():
            return redirect('/se')
        context['error'] = 'Tick information is incorrect or absent.'
        return render(request, "objects/links.html", context)


def se(request):

    if not 'answered_group' in request.session:
        pass
    else:
        if request.session['answered_group'] > 4:
            return redirect('/survey')

    if not 'condition' in request.session:
        context = {'page': 'links'}
        return render(request, "objects/links.html", context)

    context = {'page': request.session['condition']}
    context['questions'] = []
    context['browser'] = request.session['browser']
    try:
        if not 'city' in request.session:
            context['city'] = ''
            request.session['city'] = ''
        else:
            context['city'] = request.session['city']
    except Exception as e:
        context['city'] = ''
    if request.user.is_authenticated():

        user_profile = User_Profile.objects.get(user=request.user)
        context['search_results'] = []
        for search_result in user_profile.results_clicked.all():
            context['search_results'].append(search_result)

        context['client_address'] = user_profile.ip_address
        if 'qid' in request.GET:
            question = Question.objects.get(id=request.GET['qid'])
            context['question'] = question
            context['text'] = language(request, question)
            return render(request, 'objects/se.html', context)

        if not 'answered_index' in request.session:
            request.session['answered_index'] = 1
        
        if not 'answered_group' in request.session or request.session['answered_index'] <= 4:
            request.session['answered_group'] = 0
            question = Question.objects.get(id=request.session['answered_index'])
            context['question'] = question
            context['text'] = language(request, question)
            return render(request, 'objects/se.html', context)

        elif request.session['answered_index'] > 4:
            questions = Question.objects.filter(group=request.session['answered_group'])
            for question in questions:
                q = {}
                text = language(request, question)
                q['question'] = question
                q['text'] = text
                context['questions'].append(q)
            return render(request, 'objects/select.html', context)
    else:
        return redirect('/')


def submit_answer(request):

    if not 'questionid' or not 'answer' in request.POST:
        return redirect('/')

    context = {}
    qid = request.POST['questionid']
    question = Question.objects.get(id=qid)
    answer = request.POST['answer']
    if len(answer) < 1:
        messages.add_message(request, messages.INFO, 'Please do not submit a blank answer')
        return redirect('/se')
    if request.user.is_authenticated():

        user_profile = User_Profile.objects.get(user=request.user)
        context['client_address'] = user_profile.ip_address
        if Answer.objects.filter(question=question, user=request.user):
            return redirect('/')

        new_answer = Answer(question=question, user=request.user, text=answer)
        new_answer.save()
        user_profile.questions_answered.add(question)
        user_profile.answers.add(new_answer)

        if not 'answered_group' in request.session or request.session['answered_index'] < 4:
            request.session['answered_group'] = 0
            request.session['answered_index'] = request.session['answered_index'] + 1
            return redirect('/se')

        if request.session['answered_index'] == 4:
            request.session['answered_group'] = request.session['answered_group'] + 1
            request.session['answered_index'] = request.session['answered_index'] + 1
            return redirect('/se')

        elif request.session['answered_index'] > 4:
            request.session['answered_group'] = request.session['answered_group'] + 1
            return redirect('/se')


def privacy(request):
    context = {'page': 'privacy'}
    return render(request, "objects/privacy.html")


def privacy_simplified(request):
    context = {'page': 'privacy'}
    return render(request, "objects/privacy.html")


def survey(request):
    context = {'page': 'survey'}
    context['current_group'] = request.session['answered_group']
    context['questions'] = []
    questions = Question.objects.filter(group__contains=request.session['answered_group'])
    for question in questions:
        q = {}
        text = language(request, question)
        q['question'] = question
        q['text'] = text
        q['options'] = question.options.all()
        context['questions'].append(q)

    return render(request, 'objects/survey.html', context)


def submit_survey(request):
    context = {'page': 'submit_survey'}
    keys = request.POST.iterkeys()
    if request.session['answered_group'] != 5:
        for key in keys:
            if request.POST[key] == '0':
                messages.add_message(request, messages.INFO, 'Please answer all questions')
                return redirect('/survey')

    for key in keys:
        if key != 'csrfmiddlewaretoken':
            question = Question.objects.get(id=key)
            new_answer = Answer(question=question, user=request.user, text=request.POST[key])
            new_answer.save()
    request.session['answered_group'] = request.session['answered_group'] + 1
    return redirect('/survey')


def save(request):
    user_profile = User_Profile.objects.get(user=request.user)
    question = Question.objects.get(id=request.session['answered_index'])
    if request.is_ajax:
        if 'result_text' in request.POST:
            href = request.POST['result_href']
            new_href = re.search(r'(?<=q=)(.*?)(?<=&)', href)
            search_result = Search_Result(text=request.POST['result_text'], href=new_href.group(0)[:-1], user=request.user, question=question)
            search_result.save()
            user_profile.results_clicked.add(search_result)
            return HttpResponse(new_href.group(0)[:-1])
        elif 'privacy' in request.POST:
            request.session['privacy_clicked'] += 1
            user_profile.privacy_clicked = user_profile.privacy_clicked + 1
            user_profile.save()
            return HttpResponse("Here's the text of the Web page.")
        elif 'value' in request.POST:
            query = request.POST['value']
            value = Search_Query(text=query, question=question, user=request.user)
            value.save()
            user_profile.search_queries.add(value)
            return HttpResponse("Here's the text of the Web page.")
        else:
            time = datetime.now()
            user_profile.end_time = time
            user_profile.privacy_clicked = request.session['privacy_clicked']
            user_profile.save()
            return HttpResponse("Here's the text of the Web page.")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def language(request, question):
    if request.session['language'] == 'EN':
        return question.english
    if request.session['language'] == 'IT':
        return question.italian
    if request.session['language'] == 'DE':
        return question.german
    if request.session['language'] == 'PO':
        return question.polish
