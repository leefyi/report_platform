#!/usr/local/bin python
# coding=utf-8
# @Time    : 2018/8/6 下午10:51
# @Author  : lifangyi
# @File    : forms.py
# @Software: PyCharm

from django import forms
from .models import ReportUser
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ReportUserForm(forms.ModelForm):
    class Meta:
        model = ReportUser
        fields = ("address",)

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=("email",)