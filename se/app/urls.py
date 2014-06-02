from django.conf.urls import patterns, include, url

from django.conf.urls.static import static

from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^se$', 'app.views.se'),
                       url(r'^privacy$', 'app.views.privacy'),
                       url(r'^landing$', 'app.views.landing'),
                       url(r'^submit_answer$', 'app.views.submit_answer'),
                       url(r'^survey$', 'app.views.survey'),
                       url(r'^submit_survey$', 'app.views.submit_survey'),
                       url(r'^save$', 'app.views.save'),
                       url(r'^thanks$', 'app.views.thanks'),
                       url(r'^redirect$', 'app.views.redirector'),
                       url(r'^feed$', 'app.views.feed'),
                       url(r'^parse$', 'app.views.parse'),
                       url(r'^$', 'app.views.links'),
                       ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += patterns('',
    url(r'^', include('app.reporting.urls')),
    )
