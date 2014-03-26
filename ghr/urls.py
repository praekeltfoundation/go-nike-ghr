from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'skeleton.views.home', name='home'),
    # url(r'^skeleton/', include('skeleton.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^vumigo/admin/', include(admin.site.urls)),
    url(r'^vumigo/celery/', include('celery_app.urls')),

    # Monitoring and Learning urls
    url(r'^vumigo/', include('monitor_and_learn.urls')),
    # API links
    url(r'^vumigo/', include('articles.urls')),
    url(r'^vumigo/', include('user_interactions.urls')),
    url(r'^vumigo/', include('shangazi.urls')),
    url(r'^vumigo/', include('opinions.urls')),
    url(r'^vumigo/', include('weekly_quiz.urls')),
    url(r'^vumigo/', include('directory.urls')),
    url(r'^vumigo/', include('hierarchy.urls')),
)
