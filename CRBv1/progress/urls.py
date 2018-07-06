from django.urls import path, include
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ProgressView.as_view(), name="progress"),
    path('<rangeurl>/report/', views.ReportView.as_view(), name="report"),
]
