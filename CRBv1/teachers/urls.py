from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.TeacherDashboard.as_view(), name="teacherdashboard"),
<<<<<<< HEAD
    path('usermanagement/', views.UserManagement.as_view(), name="usermanagement"),
    path('usermanagement/adduser', views.AddUser.as_view(), name="adduser"),
    path('usermanagement/adduser/success', views.AddUserSuccess.as_view(), name="addusersuccess"),
    path('usermanagement/modifyuser/<username>', views.ModifyUser.as_view(), name="modifyuser"),
    path('usermanagement/deleteuser/<username>', views.DeleteUser.as_view(), name="deleteuser"),
    path('groupmanagement/', views.GroupManagement.as_view(), name="groupmanagement"),
]  
=======
    url(r'^usermanagement/$', views.UserManagement.as_view(), name="usermanagement"),
    url(r'^usermanagement/adduser$', views.AddUser.as_view(), name="adduser"),
    url(r'^usermanagement/adduser$', views.AddUser.as_view(), name="adduser"),
]
>>>>>>> bdb8423ccba0c0ca03a04d379199759b9343dedf
