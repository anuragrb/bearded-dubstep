from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^somepage$', 'app.views.somepage'),
                       url(r'^se_alt$', 'app.views.se_alt'),
                       url(r'^se_annoying$', 'app.views.se_annoying'),
                       url(r'^se_informal$', 'app.views.se_informal'),
                       url(r'^se$', 'app.views.se'),
                       url(r'^privacy$', 'app.views.privacy'),
                       url(r'^$', 'app.views.home'),
                       )
