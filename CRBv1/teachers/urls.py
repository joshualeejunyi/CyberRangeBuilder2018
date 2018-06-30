from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.TeacherDashboard.as_view(), name="teacherdashboard"),
    path('usermanagement/', views.UserManagement.as_view(), name="usermanagement"),
    path('usermanagement/adduser', views.AddUser.as_view(), name="adduser"),
    path('usermanagement/adduser/success', views.AddUserSuccess.as_view(), name="addusersuccess"),
    path('usermanagement/modifyuser/<username>', views.ModifyUser.as_view(), name="modifyuser"),
    path('usermanagement/modifyuser/<username>/resetpassword', views.ResetPasswordView.as_view(), name="modifyuser"),
    path('usermanagement/deleteuser/<username>', views.DeleteUser.as_view(), name="deleteuser"),
    path('groupmanagement/', views.GroupManagement.as_view(), name="groupmanagement"),
    path('groupmanagement/addgroup', views.AddGroup.as_view(), name="addgroup"),
    path('groupmanagement/addgroup/success', views.AddGroupSuccess.as_view(), name="addgroupsuccess"),
    path('groupmanagement/<groupname>', views.GroupView.as_view(), name="viewgroup"),
    #path('groupmanagement/<groupname>/adduser', views.AddUserInGroup.as_view(), name="adduseringroup"),
]  
