from django.urls import path, include
from django.conf.urls import url
from . import views
from django_filters.views import FilterView
from .filters import *

urlpatterns = [
    url(r'^$', views.TeacherDashboard.as_view(), name="teacherdashboard"),
    path('usermanagement/', views.UserManagement.as_view(), name="usermanagement"),
    path('usermanagement/search', FilterView.as_view(filterset_class=StudentFilter, template_name='teachers/usersearch.html'), name='search'),
    path('usermanagement/adduser', views.AddUser.as_view(), name="adduser"),
    path('usermanagement/adduser/success', views.AddUserSuccess.as_view(), name="addusersuccess"),
    path('usermanagement/modifyuser/<username>', views.ModifyUser.as_view(), name="modifyuser"),
    path('usermanagement/modifyuser/<username>/resetpassword', views.ResetPasswordView.as_view(), name="modifyuser"),
    path('usermanagement/deleteuser/<username>', views.DeleteUser.as_view(), name="deleteuser"),
    path('groupmanagement/', views.GroupManagement.as_view(), name="groupmanagement"),
    path('groupmanagement/deletegroup/<groupname>', views.DeleteGroup.as_view(), name="deletegroup"),
    path('groupmanagement/addgroup', views.AddGroup.as_view(), name="addgroup"),
    path('groupmanagement/addgroup/success', views.AddGroupSuccess.as_view(), name="addgroupsuccess"),
    path('groupmanagement/<groupname>/', views.GroupView.as_view(), name="viewgroup"),
    path('groupmanagement/<groupname>/makeleader/<username>', views.MakeLeader.as_view(), name="makeleader"),
    path('groupmanagement/<groupname>/remove/<username>', views.RemoveStudentFromGroup.as_view(), name="removestudentfromgroup"),
    path('groupmanagement/<groupname>/addusers', views.AddUserInGroup.as_view(), name="adduseringroup"),
    path('groupmanagement/<groupname>/addusers/<username>', views.AddUserToCart.as_view(), name="addusertocart"),
    path('groupmanagement/<groupname>/removeusers/<username>', views.RemoveUserFromCart.as_view(), name="removeuserfromcart"),
    path('groupmanagement/<groupname>/commit', views.UserGroupCommit.as_view(), name="usergroupcommit"),
    path('groupmanagement/deletegroup/', views.UserGroupCommit.as_view(), name="usergroupcommit"),

    # hi
    path('rangemanagement/', views.RangeManagement.as_view(), name='rangemanagement'),
    path('rangemanagement/createrange/', views.CreateRange.as_view(), name="createrange"),
    path('rangemanagement/createrange/createquestion/', views.CreateQuestion.as_view(), name="createquestion"),
    path('rangemanagement/<rangename>', views.RangeView.as_view(), name="rangeview"),
    path('rangemanagement/deleterange/<rangeid>', views.DeleteRange.as_view(), name="deleterange"),
    path('rangemanagement/viewquestion/<rangeid>/<questionid>', views.EditQuestion.as_view(), name="editquestion"),    
]  
