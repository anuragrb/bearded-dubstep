from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^somepage$', 'app.views.somepage'),
                       url(r'^se_alt$', 'app.views.se_alt'),
                       url(r'^se$', 'app.views.se'),
                       url(r'^$', 'app.views.home'),
                       )
