from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as authviews
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', login_required(views.DashboardView.as_view()), name="dashboard"),
]
