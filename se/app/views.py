from django.shortcuts import render

from django.http import HttpRequest  
  
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
    return render(request, "objects/se.html", context)


def se_traditional(request):
    context = {'page': 'se_traditional'}
    return render(request, "objects/se.html", context)


def se_anthropomorphic(request):
    context = {'page': 'se_anthropomorphic'}
    return render(request, "objects/se.html", context)


def se_informal(request):
    context = {'page': 'se_informal'}
    return render(request, "objects/se.html", context)


def se_tracking(request):
    context = {'page': 'se_tracking'}
    return render(request, "objects/se.html", context)


def se_static(request):
    context = {'page': 'se_static'}
    return render(request, "objects/se.html", context)


def se_ip(request):
    context = {'page': 'se_ip'}
    context['client_address'] = request.META.get('REMOTE_ADDR')
    return render(request, "objects/se.html", context)


def privacy(request):
    context = {'page': 'privacy'}
    return render(request, "objects/privacy.html")
