from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as authviews

from . import views

urlpatterns = [
    # path('', views.LoginFormView, name='login'),
    url(r'^$', views.DashboardView.as_view(), name="dashboard"),
]
