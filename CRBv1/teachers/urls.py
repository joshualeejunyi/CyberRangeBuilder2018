from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.TeacherDashboard.as_view(), name="teacherdashboard"),
    url(r'^usermanagement/$', views.UserManagement.as_view(), name="usermanagement"),
    url(r'^usermanagement/adduser$', views.AddUser.as_view(), name="adduser"),
    url(r'^usermanagement/adduser$', views.AddUser.as_view(), name="adduser"),
]