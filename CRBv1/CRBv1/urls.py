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
from exapi02 import views
from ranges import views as rangesview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', authviews.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^$', authviews.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'loginsuccess/$', account.LoginRedirect.loginsuccess, name='loginredirect'),
    url(r'^logout/$', authviews.logout, {'next_page': '/login'}, name='logout'),
    url(r'^register/success/$', account.RegistrationSucess.as_view(), name='registrationsuccess'),
    url(r'^dashboard/', include('dashboard.urls'), name='dashboard'),
    url(r'^ranges/', include('ranges.urls'), name='ranges'),
    url(r'^teachers/', include('teachers.urls'), name='teachers'),
    path('createcon/', views.home),
    path('error/', rangesview.ErrorMessage.as_view(), name='error')
]
