# -*- coding: utf-8 -*-
"""djproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from jobs.views import hello
from jobs import views as jobs_views

import xadmin 
xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = [
    #url(r'^$', include(admin.site.urls)),
    url('^$', jobs_views.hello),
    url(r'^admin/', include(admin.site.urls)),
    #url('^hello/$', include(jobs.hello)),
    url('^hello/$', hello),
    url(r'^add/$', jobs_views.add, name='add'),
    url(r'^index/$', jobs_views.index,name='home'),
    url(r'^add/(\d+)/(\d+)/$', jobs_views.add2, name='add2'),
    url(r'^polls/', include('jobs.urls', namespace="polls")),
    url(r'xadmin/', include(xadmin.site.urls)),

]
