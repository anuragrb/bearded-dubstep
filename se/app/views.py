from django.shortcuts import render

# Create your views here.

def home(request):
    context = {'page': 'home'}
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


def privacy(request):
    context = {'page': 'privacy'}
    return render(request, "objects/privacy.html")
