# Python library imports
from datetime import datetime
import re
import random
import string

# Django specific imports
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests
import logging

# App specific imports
from generate_question import generate_question
from app.models import *

logger = logging.getLogger('custom.logger')


def links(request):
    context = {'page': 'links'}
    if 'tick' in request.GET:

        if User.objects.filter(username=request.GET['tick']):

            if request.user.is_authenticated():
                return redirect('/se')
            else:
                user = authenticate(username=request.GET['tick'], password='')
                login(request, user)
                return redirect('/se')
        else:

            new_user = User.objects.create_user(username=request.GET['tick'], password='')
            new_user.save()
            if len(request.GET['tick']) > 30:
                tick = request.GET['tick'][0:30]
            else:
                tick = request.GET['tick']
            user = authenticate(username=tick, password='')
            login(request, user)
            request.session['username'] = tick
            try:
                r = requests.get(
                    'http://freegeoip.net/csv/' + get_client_ip(request))
                city = r.text.split(',')[5]
                city = city[1:-1]
                if len(city) < 1:
                    request.session['city'] = ''
                else:
                    request.session['city'] = city
            except Exception as e:
                logger.exception(
                    'There was a key error while retrieving a city or country from freegeoip.net')
                city = ''
                request.session['city'] = ''
            new_profile = User_Profile(user=new_user, tick=tick, ip_address=get_client_ip(request), privacy_clicked=0, city=city)
            request.session['privacy_clicked'] = 0
            new_profile.save()
            if 'C' in request.GET:
                country = str(request.GET['C'])
                if country == '1':
                    request.session['country'] = 'UK'
                    request.session['language'] = 'EN'
                elif country == '2':
                    request.session['country'] = 'Germany'
                    request.session['language'] = 'DE'
                elif country == '3':
                    request.session['country'] = 'Poland'
                    request.session['language'] = 'PO'
                elif country == '4':
                    request.session['country'] = 'Italy'
                    request.session['language'] = 'IT'
            else:
                request.session['country'] = 'Undefined'
                request.session['language'] = 'EN'
            condition = random.randint(1, 8)
            request.session['conint'] = condition
            return redirect('/landing')

    elif 'workerId' in request.GET:

        return render(request, 'objects/mturk_landing.html')

    else:        
        if request.user.is_authenticated():
            return redirect('/se')
        context['error'] = 'Tick information is incorrect or absent.'
        return render(request, "objects/links.html", context)


def landing(request):

    context = {'page': 'landing'}
    if request.user.is_authenticated():

        EXPERIMENTAL_CONDITIONS = {
            '1': 'TR',
            '2': 'CO',
            '3': 'AN',
            '4': 'ST',
            '5': 'IP',
            '6': 'CL',
            '7': 'IN',
            '8': 'SI'
        }
        user_profile = User_Profile.objects.get(user=request.user)
        try:
            condition = EXPERIMENTAL_CONDITIONS[str(request.session['conint'])]
            context['condition'] = condition
            request.session['condition'] = condition
            user_profile.experimental_condition = condition
        except Exception as e:
            logger.exception('Randomizer key error')
            return redirect('/')
        if not 'language' in request.session:
            request.session['language'] = 'EN'
            user_profile.country = 'Undefined'
        else:
            user_profile.country = request.session['country']
        if not 'screen_resolution' in request.session:
            user_profile.screen_resolution = ''
        else:
            user_profile.screen_resolution = request.session['screen_resolution']

        if not 'browser_resolution' in request.session:
            user_profile.browser_resolution = ''
        else:
            user_profile.browser_resolution = request.session['browser_resolution']

        if not 'browser' in request.session:
            user_profile.browser = ''
        else:
            user_profile.browser = request.session['browser']

        user_profile.save()
        return render(request, "objects/landing.html", context)
    else:
        return redirect('/')


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
    try:
        if not 'browser' in request.session:
            context['browser'] = 'Internet Explorer'
        else:
            context['browser'] = request.session['browser']
        if not 'city' in request.session:
            context['city'] = ''
            request.session['city'] = ''
        else:
            context['city'] = request.session['city']
    except Exception as e:
        logger.exception(
            'No city in request.session or no browser in request.session. Traceback has more details')
        context['city'] = ''

    if request.user.is_authenticated():

        user_profile = User_Profile.objects.get(user=request.user)
        context['search_results'] = []            

        for search_result in user_profile.results_clicked.all():
            context['search_results'].append(search_result)

        context['client_address'] = user_profile.ip_address
        if 'qid' in request.GET:
            question = Question.objects.get(id=request.GET['qid'])
            request.session['answered_index'] = request.GET['qid']
            context['question'] = question
            context['text'] = language(request, question)
            return render(request, 'objects/se.html', context)

        if not 'answered_index' in request.session:
            user_profile.begin_time = datetime.now()
            user_profile.save()
            request.session['answered_index'] = 1

        if not 'answered_group' in request.session or request.session['answered_index'] <= 4:
            request.session['answered_group'] = 0
            question = Question.objects.get(
                id=request.session['answered_index'])
            context['question'] = question
            context['text'] = language(request, question)
            return render(request, 'objects/se.html', context)

        elif request.session['answered_index'] > 4:
            questions = Question.objects.filter(
                group=request.session['answered_group'])
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
    clicktime = request.POST['clicktime']

    if request.user.is_authenticated():

        user_profile = User_Profile.objects.get(user=request.user)
        context['client_address'] = user_profile.ip_address
        if Answer.objects.filter(question=question, user=request.user):
            return redirect('/')

        if 'difference' in request.session:
            new_answer = Answer(question=question, user=request.user, text=answer, clicktime=clicktime, select_time=request.session['difference'])
        else:
            new_answer = Answer(question=question, user=request.user, text=answer, clicktime=clicktime)

        new_answer.save()
        user_profile.questions_answered.add(question)
        user_profile.answers.add(new_answer)

        if not 'answered_group' in request.session or request.session['answered_index'] < 4:
            request.session['answered_group'] = 0
            request.session['answered_index'] = request.session[
                'answered_index'] + 1
            return redirect('/se')

        if request.session['answered_index'] == 4:
            request.session['answered_group'] = request.session[
                'answered_group'] + 1
            request.session['answered_index'] = request.session[
                'answered_index'] + 1
            return redirect('/se')

        elif request.session['answered_index'] > 4:
            request.session['answered_group'] = request.session[
                'answered_group'] + 1
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
    user_profile = User_Profile.objects.get(user=request.user)
    questions = Question.objects.filter(
        group=request.session['answered_group'])
    context['user_profile'] = user_profile
    for question in questions:
        q = {}
        text = language(request, question)
        q['question'] = question
        q['text'] = text
        q['options'] = question.options.all()
        q['category'] = question.category
        context['questions'].append(q)

    return render(request, 'objects/survey.html', context)


def submit_survey(request):
    context = {'page': 'submit_survey'}
    if request.is_ajax:
        try:
            keys = request.POST.iterkeys()

            for key in keys:
                if key != 'csrfmiddlewaretoken':
                    question = Question.objects.get(id=key)
                    new_answer = Answer(
                        question=question, user=request.user, text=request.POST[key])
                    new_answer.save()
                    if str(key) == '69':
                        user_profile = User_Profile.objects.get(user=request.user)
                        user_profile.completed = 1
                        user_profile.save()

            request.session['answered_group'] = request.session['answered_group'] + 1
        except Exception as e:
            logger.exception('Something terrible happened while saving survey data. Check stack trace')
        return redirect('/survey')


def save(request):
    user_profile = User_Profile.objects.get(user=request.user)
    if 'answered_index' in request.session:
        question = Question.objects.get(id=request.session['answered_index'])
    else:
        question = ''
    if request.is_ajax:
        try:
            if 'result_text' in request.POST:
                href = request.POST['result_href']
                new_href = re.search(r'(?<=q=)(.*?)(?<=&)', href)
                search_result = Search_Result(
                    text=request.POST['result_text'], href=new_href.group(0)[:-1], user=request.user, question=question)
                search_result.save()
                user_profile.results_clicked.add(search_result)
                return HttpResponse(new_href.group(0)[:-1])
            elif 'screenresolution' in request.POST:
                screen_resolution = request.POST['screenresolution']
                browser_resolution = request.POST['browserresolution']
                browser = request.POST['browser']
                request.session['screen_resolution'] = screen_resolution
                request.session['browser_resolution'] = browser_resolution
                request.session['browser'] = browser
                user_profile.screen_resolution = screen_resolution
                user_profile.browser_resolution = browser_resolution
                user_profile.browser = browser
                user_profile.save()
                return HttpResponse('Done')
            elif 'privacy' in request.POST:
                request.session['privacy_clicked'] += 1
                user_profile.privacy_clicked = user_profile.privacy_clicked + 1
                user_profile.save()
                return HttpResponse("Successfully incremented privacy counter.")
            elif 'value' in request.POST:
                query = request.POST['value']
                value = Search_Query(
                    text=query, question=question, user=request.user)
                value.save()
                user_profile.search_queries.add(value)
                return HttpResponse("Successfully added a new search query.")
            elif 'hasflash' in request.POST:
                user_profile.hasflash = request.POST['hasflash']
                user_profile.save()
                return HttpResponse("Successfully checked for flash in user's browser.")
            elif 'difference' in request.POST:
                request.session['difference'] = request.POST['difference']
                return HttpResponse("Saved current difference to session.")
            else:
                time = datetime.now()
                user_profile.end_time = time
                user_profile.privacy_clicked = request.session['privacy_clicked']
                user_profile.mturk_payment_code = id_generator()
                user_profile.save()
                request.session['mturk_payment_code'] = user_profile.mturk_payment_code
                return HttpResponse("Successfully completed the survey for the current user.")
        except Exception as e:
            logger.exception('Something very bad happened while saving to the DB')


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


def thanks(request):
    return render(request, 'objects/thanks.html')


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


#Unrelated to search engine project
def feed(request):

    if 'ipaddress' in request.GET:
        data = request.GET['ipaddress']
    else:
        data = ''
    r = requests.get(
                    'http://freegeoip.net/csv/' + data)

    print r
    data = r.text.split(',')[6]
    data = data[1:-1]

    new_data = ''

    if len(data) == 5:

        i = 0
        while i < len(data):

            if i < 2:
                new_data = new_data + data[i]
            else:
                new_data = new_data + '*'
            i = i + 1

    if len(data) >= 6:

        i = 0
        while i < len(data):

            if i < 3:
                new_data = new_data + data[i]
            else:
                new_data = new_data + '*'
            i = i + 1

    return render(request, 'objects/feed.xml', {'data':new_data})


def parse(request):
    #"128.237.182.187","US","United States","PA","Pennsylvania","Pittsburgh","15213","40.4439","-79.9561","508","412"
    if 'ipaddress' in request.GET:
        data = request.GET['ipaddress']
    else:
        data = ''
    r = requests.get(
                    'http://freegeoip.net/csv/' + data)
    r = r.text.split(',')
    country = r[2][1:-1]
    zipcode = r[6][1:-1]
    state = r[4][1:-1]
    city = r[5][1:-1]

    context['country'] = country
    context['zipcode'] = zipcode
    context['state'] = state
    context['city'] = city
    return render(request, 'objects/parse.xml', context)