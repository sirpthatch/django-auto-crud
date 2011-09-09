from django.db.models import get_app, get_models
from django.conf.urls.defaults import patterns, include, url
from djangocrud import requests

urlpatterns = patterns('',
    url(r'(?P<appname>.*?)/(?P<operation>(create|read|update|delete))/(?P<modelname>(\w+))', requests.handle_request),
)
