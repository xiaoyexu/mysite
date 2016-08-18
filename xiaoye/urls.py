__author__ = 'xuxiaoye'
from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^jsonResult$', views.jsonResult, name='jsonResult'),

    url(r'^.*$', views.index, name='index'),
]
