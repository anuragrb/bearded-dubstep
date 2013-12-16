from django.shortcuts import render

from django.http import HttpRequest  

from generate_question import generate_question
  
# Create your views here.

def landing(request):
    context = {'page': 'landing'}
    condition = request.GET['q']
    context['condition'] = condition
    return render(request, "objects/landing.html", context)


def links(request):
    context = {'page': 'links'}
    return render(request, "objects/links.html", context)


def se_control(request):
    context = {'page': 'se_control'}
    index = request.GET['index']
    context['index'] = index
    if 'question' in request.GET:
        context['question'] = request.GET['question']
        return render(request, 'objects/se.html', context)
    question = generate_question(index)
    context['question'] = question
    if question == 'Done':
        return render(request, 'objects/questionnaire.html', context)
    if type(question) == list:
        return render(request, 'objects/select.html', context)
    else:    
        return render(request, "objects/se.html", context)


def se_traditional(request):
    context = {'page': 'se_traditional'}
    index = request.GET['index']
    context['index'] = index
    if 'question' in request.GET:
        context['question'] = request.GET['question']
        return render(request, 'objects/se.html', context)
    question = generate_question(index)
    context['question'] = question
    if question == 'Done':
        return render(request, 'objects/questionnaire.html', context)
    if type(question) == list:
        return render(request, 'objects/select.html', context)
    else:    
        return render(request, "objects/se.html", context)


def se_anthropomorphic(request):
    context = {'page': 'se_anthropomorphic'}
    index = request.GET['index']
    context['index'] = index
    if 'question' in request.GET:
        context['question'] = request.GET['question']
        return render(request, 'objects/se.html', context)
    question = generate_question(index)
    context['question'] = question
    if question == 'Done':
        return render(request, 'objects/questionnaire.html', context)
    if type(question) == list:
        return render(request, 'objects/select.html', context)
    else:    
        return render(request, "objects/se.html", context)


def se_informal(request):
    context = {'page': 'se_informal'}
    index = request.GET['index']
    context['index'] = index
    if 'question' in request.GET:
        context['question'] = request.GET['question']
        return render(request, 'objects/se.html', context)
    question = generate_question(index)
    context['question'] = question
    if question == 'Done':
        return render(request, 'objects/questionnaire.html', context)
    if type(question) == list:
        return render(request, 'objects/select.html', context)
    else:    
        return render(request, "objects/se.html", context)


def se_tracking(request):
    context = {'page': 'se_tracking'}
    index = request.GET['index']
    context['index'] = index
    if 'question' in request.GET:
        context['question'] = request.GET['question']
        return render(request, 'objects/se.html', context)
    question = generate_question(index)
    context['question'] = question
    if question == 'Done':
        return render(request, 'objects/questionnaire.html', context)
    if type(question) == list:
        return render(request, 'objects/select.html', context)
    else:    
        return render(request, "objects/se.html", context)


def se_static(request):
    context = {'page': 'se_static'}
    index = request.GET['index']
    context['index'] = index
    if 'question' in request.GET:
        context['question'] = request.GET['question']
        return render(request, 'objects/se.html', context)
    question = generate_question(index)
    context['question'] = question
    if question == 'Done':
        return render(request, 'objects/questionnaire.html', context)
    if type(question) == list:
        return render(request, 'objects/select.html', context)
    else:    
        return render(request, "objects/se.html", context)


def se_ip(request):
    context = {'page': 'se_ip'}
    index = request.GET['index']
    context['index'] = index
    if 'question' in request.GET:
        context['question'] = request.GET['question']
        return render(request, 'objects/se.html', context)
    question = generate_question(index)
    context['question'] = question
    if question == 'Done':
        return render(request, 'objects/questionnaire.html', context)
    if type(question) == list:
        return render(request, 'objects/select.html', context)
    else:    
        context['client_address'] = request.META.get('REMOTE_ADDR')
    return render(request, "objects/se.html", context)


def se_simplified(request):
    context = {'page': 'se_simplified'}
    index = request.GET['index']
    context['index'] = index
    if 'question' in request.GET:
        context['question'] = request.GET['question']
        return render(request, 'objects/se.html', context)
    question = generate_question(index)
    context['question'] = question
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
