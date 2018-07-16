from django.urls import path, include
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ModifyUser.as_view(), name="settings"),
    path('resetpassword/', views.ResetPassword.as_view(), name="resetpassword"),
    path('success/', views.ModifyUserSuccess.as_view(), name="success"),
]
