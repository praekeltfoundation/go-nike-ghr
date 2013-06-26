from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^articles/$', 'articles.views.get_articles'),
)
