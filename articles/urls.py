from django.conf.urls import patterns, url, include
from articles.api import ArticleResource
from tastypie.api import Api

api_resources = Api(api_name='api')
api_resources.register(ArticleResource())
api_resources.prepend_urls()
urlpatterns = patterns('',
    url(r'^', include(api_resources.urls))
)
