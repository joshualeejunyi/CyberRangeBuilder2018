from django.urls import path, include
from django.conf.urls import url

from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(views.ProgressView.as_view()), name="progress"),
    path('<rangeurl>/report/', login_required(views.ReportView.as_view()), name="report"),
]
