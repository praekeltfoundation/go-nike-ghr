from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^article/$', 'articles.views.get_article'),
)
