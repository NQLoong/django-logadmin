"""LogAdmin URL Configuration

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
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from LogAdmin.view import *
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index', index_handle),
    url(r'^login$',login_page),
    url(r'^login_handle$',login_handle),
    url(r'^logout$',logoutuser),
    url(r'^ajax/register$',ajax_register),

    url(r'^ajax/addUser$',ajax_addUser),
    url(r'^ajax/revUser$',ajax_revUser),
    url(r'^ajax/delUser$',ajax_delUser),
    url(r'^ajax/revPasswd$',ajax_revPasswd),


    url(r'^ajax/revPro$',ajax_revPro),
    url(r'^ajax/addPro',ajax_addPro),
    url(r'^ajax/delPro',ajax_delPro),

    url(r'^ajax/addHost$', ajax_addHost),
    url(r'^ajax/revHost$', ajax_revHost),
    url(r'^ajax/delHost$', ajax_delHost),

    url(r'^ajax/refOption$', ajax_refOption),
    url(r'^ajax/getSelect$', ajax_getSelect),

    url(r'^ajax/addApp$', ajax_addApp),
    url(r'^ajax/revApp$', ajax_revApp),
    url(r'^ajax/delApp$', ajax_delApp),


    url(r'^ajax/showAppul',ajax_showAppul),
    url(r'^ajax/showLogul',ajax_showLogul),
    url(r'^ajax/refLog$',ajax_refLog),
    url(r'^ajax/showLogDetail$',ajax_showLogDetail),
    url(r'^ajax/refAwk$',ajax_refAwk),
    url(r'^ajax/grepLog$',ajax_grepLog),


]
