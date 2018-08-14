#!/usr/local/bin python
# coding=utf-8
# @Time    : 2018/8/6 下午10:29
# @Author  : lifangyi
# @File    : urls.py
# @Software: PyCharm

from django.urls import re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    re_path(r'^$', views.user_login, name='user_login'),
    re_path(r'^login/$', views.user_login,  name='user_login'),
    re_path(r'^logout/$', views.user_logout, name='user_logout'),
    re_path(r'reportDetail/$', views.reportDetail, name='reportDetail'),
    re_path(r'reportMore/$', views.reportMore, name='more_charts'),
    re_path(r'reportCount/$', views.reportCount, name='reportCount'),
    re_path(r'reportCount/reportCaseInfo/$', views.reportCaseInfo, name='reportCaseInfo'),
    re_path(r'^reportInfo/$', views.reportInfoListView.as_view()),
]
