#URLs file here
from django.conf.urls import patterns, include, url

from django.conf.urls.static import static

from django.conf import settings

urlpatterns = patterns('',
                       url(r'^reporting$', 'app.reporting.views.reporting'),
                       )