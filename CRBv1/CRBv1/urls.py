"""CRBv1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as authviews
from accounts import views as account
from ranges import views as rangesview
from django.contrib.auth.decorators import login_required
from accounts.forms import *

urlpatterns = [
    path('login/', authviews.LoginView.as_view(template_name='accounts/login.html', authentication_form=CheckUserDisabled), name='login'), 
    url(r'^$', authviews.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'loginsuccess/$', account.LoginRedirect.loginsuccess, name='loginredirect'),
    url(r'^logout/$', authviews.logout, {'next_page': '/login'}, name='logout'),
    url(r'register/$', account.RegisterView.as_view(), name='register'),
    url(r'^register/success/$', account.RegistrationSucess.as_view(), name='registrationsuccess'),
    url(r'^dashboard/', include('dashboard.urls'), name='dashboard'),
    url(r'^ranges/', include('ranges.urls'), name='ranges'),
    url(r'^teachers/', include('teachers.urls'), name='teachers'),
    url(r'^progress/', include('progress.urls'), name='progress'),
    url(r'^settings/', include('settings.urls'), name='settings'),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^selfdirected/', include('SDL.urls'), name='SDL'),
]
