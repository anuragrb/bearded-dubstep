from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^somepage$', 'app.views.somepage'),
                       url(r'^se_control$', 'app.views.se_control'),
                       url(r'^se_anthropomorphic$', 'app.views.se_anthropomorphic'),
                       url(r'^se_informal$', 'app.views.se_informal'),
                       url(r'^se_traditional$', 'app.views.se_traditional'),
                       url(r'^se_ip$', 'app.views.se_ip'),
                       url(r'^se_tracking$', 'app.views.se_tracking'),
                       url(r'^privacy$', 'app.views.privacy'),
                       url(r'^links$', 'app.views.links'),
                       url(r'^$', 'app.views.home'),
                       )
