from django.urls import path, include
from django.conf.urls import url
from . import views
from django_filters.views import FilterView
from .filters import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(views.TeacherDashboard.as_view()), name="teacherdashboard"),
    path('usermanagement/', login_required(views.UserManagement.as_view()), name="usermanagement"),
    path('usermanagement/search', login_required(FilterView.as_view(filterset_class=StudentFilter, template_name='teachers/usersearch.html')), name='search'),
    path('usermanagement/adduser', login_required(views.AddUser.as_view()), name="adduser"),
    path('usermanagement/adduser/success', login_required(views.AddUserSuccess.as_view()), name="addusersuccess"),
    path('usermanagement/modifyuser/<username>', login_required(views.ModifyUser.as_view()), name="modifyuser"),
    path('usermanagement/modifyuser/<username>/resetpassword', login_required(views.ResetPasswordView.as_view()), name="modifyuser"),
    path('usermanagement/disableuser/<username>', login_required(views.DisableUser.as_view()), name="disableuser"),
    path('usermanagement/acceptuser/<username>', login_required(views.AcceptUser.as_view()), name="acceptuser"),
    path('usermanagement/enableuser/<username>', login_required(views.EnableUser.as_view()), name="enableuser"),
    path('usermanagement/disabled', login_required(views.DisabledUserManagement.as_view()), name="disabledusersmanagement"),
    path('usermanagement/deleteuser/<username>', login_required(views.DeleteUser.as_view()), name="deleteuser"),
    path('groupmanagement/', login_required(views.GroupManagement.as_view()), name="groupmanagement"),
    path('groupmanagement/deletegroup/<groupname>', login_required(views.DeleteGroup.as_view()), name="deletegroup"),
    path('groupmanagement/addgroup', login_required(views.AddGroup.as_view()), name="addgroup"),
    path('groupmanagement/addgroup/success', login_required(views.AddGroupSuccess.as_view()), name="addgroupsuccess"),
    path('groupmanagement/<groupname>/', login_required(views.GroupView.as_view()), name="viewgroup"),
    path('groupmanagement/<groupname>/makeleader/<username>', login_required(views.MakeLeader.as_view()), name="makeleader"),
    path('groupmanagement/<groupname>/remove/<username>', login_required(views.RemoveStudentFromGroup.as_view()), name="removestudentfromgroup"),
    path('groupmanagement/<groupname>/addusers', login_required(views.AddUserInGroup.as_view()), name="adduseringroup"),
    path('groupmanagement/<groupname>/addusers/<username>', login_required(views.AddUserToCart.as_view()), name="addusertocart"),
    path('groupmanagement/<groupname>/removeusers/<username>', login_required(views.RemoveUserFromCart.as_view()), name="removeuserfromcart"),
    path('groupmanagement/<groupname>/commit', login_required(views.UserGroupCommit.as_view()), name="usergroupcommit"),
    path('groupmanagement/deletegroup/', login_required(views.UserGroupCommit.as_view()), name="usergroupcommit"),

    # hi
    path('rangemanagement/', login_required(views.RangeManagement.as_view()), name='rangemanagement'),
    path('rangemanagement/createrange/', login_required(views.CreateRange.as_view()), name="createrange"),
    path('rangemanagement/createrange/createquestion/', login_required(views.CreateQuestion.as_view()), name="createquestion"),
    path('rangemanagement/view/<rangeurl>', login_required(views.RangeView.as_view()), name="rangeview"),
    path('rangemanagement/deleterange/<rangeid>', login_required(views.DeleteRange.as_view()), name="deleterange"),
    path('rangemanagement/viewquestion/<rangeid>/edit/<questionid>', login_required(views.EditQuestion.as_view()), name="editquestion"),
]  