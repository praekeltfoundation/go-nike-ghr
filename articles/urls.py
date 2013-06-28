from django.conf.urls import patterns, url, include
from articles.api import ArticleResource

article_resource = ArticleResource()

urlpatterns = patterns('',
    url(r'^', include(article_resource.urls))
)
