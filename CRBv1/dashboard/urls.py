from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as authviews

from . import views

urlpatterns = [
    url(r'^$', views.DashboardView.as_view(), name="dashboard"),
]
