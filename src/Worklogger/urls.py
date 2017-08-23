"""Worklogger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout

from profiles import views as profile_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', profile_views.login, name="home"),
    url(r'^login/$', profile_views.login, name="login"),
    url(r'^login-information/$', profile_views.login_information, name="login_information"),
    url(r'^register/$', profile_views.register, name="register"),
    url(r'^home/$', profile_views.home, name="home"),
    url(r'^project-add/$', profile_views.add_project, name="add_project"),
    url(r'^logout/$', logout, {'template_name': 'profiles/account/logout_user.html'}, name ='logout'),

]
