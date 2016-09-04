__author__ = 'xuxiaoye'
from django.conf.urls import url
from . import views

urlpatterns = [
    # Json APIs
    url(r'^jsonResult$', views.jsonResult, name='jsonResult'),
    url(r'^api\/login$', views.apiLogin, name='apiLogin'),
    url(r'^rs$', views.rs, name='rs'),
    # End of Json APIs
    # Wechat backend
    url(r'^weixin$', views.weixin, name='weixin'),
    # End of Wechat backend
    # Common process
    url(r'^back$', views.back, name='back'),
    url(r'^logoff$', views.logoff, name='logoff'),
    # End of Common process
    # Application pages
    url(r'^app1\_1$', views.app1_1, name='app1_1'),
    url(r'^app1\_2$', views.app1_2, name='app1_2'),
    url(r'^app2\_1$', views.app2_1, name='app2_1'),
    # End of Application pages
    # Ajax
    url(r'^ajax$', views.ajax, name='ajax'),
    # End of Ajax
    # Default home page
    url(r'^.*$', views.index, name='index'),
    # End of Default home page
]
