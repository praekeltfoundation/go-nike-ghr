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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^celery/', include('celery_app.urls')),

    # Monitoring and Learning urls
    url(r'^', include('monitor_and_learn.urls')),
    # API links
    url(r'^', include('articles.urls')),
    url(r'^', include('user_interactions.urls')),
    url(r'^', include('ndabaga.urls')),
    url(r'^', include('opinions.urls')),
    url(r'^', include('weekly_quiz.urls')),
    url(r'^', include('directory.urls')),
)
