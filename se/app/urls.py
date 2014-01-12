from django.conf.urls import patterns, include, url

from django.conf.urls.static import static

from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^somepage$', 'app.views.somepage'),
                       url(r'^se$', 'app.views.se'),
                       url(r'^privacy$', 'app.views.privacy'),
                       url(r'^landing$', 'app.views.landing'),
                       url(r'^$', 'app.views.links'),
                       ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
