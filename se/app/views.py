from django.shortcuts import render

# Create your views here.


def home(request):
    context = {'page': 'home'}
    return render(request, "objects/links.html", context)


def somepage(request):
    context = {'page': 'somepage'}
    return render(request, "objects/somepage.html", context)


def se(request):
    context = {'page': 'se'}
    return render(request, "objects/se.html", context)


def se_alt(request):
    context = {'page': 'se_alt'}
    return render(request, "objects/se.html", context)


def se_annoying(request):
    context = {'page': 'se_annoying'}
    return render(request, "objects/se.html", context)


def se_informal(request):
    context = {'page': 'se_informal'}
    return render(request, "objects/se.html", context)
