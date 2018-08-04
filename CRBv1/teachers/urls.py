from django.urls import path, include
from django.conf.urls import url
from . import views
from settings import views as settingview
from django_filters.views import FilterView
from .filters import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(views.TeacherDashboard.as_view()), name="teacherdashboard"),

    # USER MANAGEMENT
    path('usermanagement/', login_required(views.UserManagement.as_view()), name="usermanagement"),
    path('usermanagement/search/', login_required(FilterView.as_view(filterset_class=StudentFilter, template_name='teachers/usersearch.html')), name='search'),
    path('usermanagement/adduser/', login_required(views.AddUser.as_view()), name="adduser"),
    path('usermanagement/adduser/success/', login_required(views.AddUserSuccess.as_view()), name="addusersuccess"),
    path('usermanagement/modifyuser/<username>/', login_required(views.ModifyUser.as_view()), name="modifyuser"),
    path('usermanagement/modifyuser/<username>/resetpassword', login_required(views.ResetPasswordView.as_view()), name="modifyuser"),
    path('usermanagement/disableuser/<username>/', login_required(views.DisableUser.as_view()), name="disableuser"),
    path('usermanagement/acceptuser/<username>/', login_required(views.AcceptUser.as_view()), name="acceptuser"),
    path('usermanagement/rejectuser/<username>/', login_required(views.RejectUser.as_view()), name="rejectuser"),
    path('usermanagement/enableuser/<username>/', login_required(views.EnableUser.as_view()), name="enableuser"),
    path('usermanagement/disabled', login_required(views.DisabledUserManagement.as_view()), name="disabledusersmanagement"),
    path('usermanagement/deleteuser/<username>/', login_required(views.DeleteUser.as_view()), name="deleteuser"),

    # GROUP MANAGEMENT
    path('groupmanagement/', login_required(views.GroupManagement.as_view()), name="groupmanagement"),
    path('groupmanagement/deletegroup/<groupname>/', login_required(views.DeleteGroup.as_view()), name="deletegroup"),
    path('groupmanagement/addgroup/', login_required(views.AddGroup.as_view()), name="addgroup"),
    path('groupmanagement/addgroup/success/', login_required(views.AddGroupSuccess.as_view()), name="addgroupsuccess"),
    path('groupmanagement/<groupname>/', login_required(views.GroupView.as_view()), name="viewgroup"),
    path('groupmanagement/<groupname>/makeleader/<username>/', login_required(views.MakeLeader.as_view()), name="makeleader"),
    path('groupmanagement/<groupname>/remove/<username>/', login_required(views.RemoveStudentFromGroup.as_view()), name="removestudentfromgroup"),
    path('groupmanagement/<groupname>/addusers/', login_required(views.AddUserInGroup.as_view()), name="adduseringroup"),
    path('groupmanagement/<groupname>/addusers/add/<username>/', login_required(views.AddUserToCart.as_view()), name="addusertocart"),
    path('groupmanagement/<groupname>/addusers/remove/<username>/', login_required(views.RemoveUserFromCart.as_view()), name="removeuserfromcart"),
    path('groupmanagement/<groupname>/addusers/commit/', login_required(views.UserGroupCommit.as_view()), name="usergroupcommit"),
    path('groupmanagement/deletegroup/', login_required(views.UserGroupCommit.as_view()), name="usergroupcommit"),

    # RANGE MANAGEMENT
    path('rangemanagement/', login_required(views.RangeManagement.as_view()), name='rangemanagement'),
    path('rangemanagement/createrange/', login_required(views.CreateRange.as_view()), name="createrange"),
    path('rangemanagement/createrange/<rangeurl>/createquestion/', login_required(views.CreateQuestion.as_view()), name="createquestion"),
    path('rangemanagement/view/<rangeurl>/createquestion/', login_required(views.CreateQuestion.as_view()), name="createquestion"),
    path('rangemanagement/view/<rangeurl>/createquestion/MCQ/', login_required(views.CreateMCQQuestion.as_view()), name="createmcqquestion"),
    path('rangemanagement/view/<rangeurl>/createquestion/TF/', login_required(views.CreateTFQuestion.as_view()), name="createtfquestion"),
    path('rangemanagement/view/<rangeurl>/createquestion/FL/', login_required(views.CreateFLQuestion.as_view()), name="createflquestion"),
    path('rangemanagement/view/<rangeurl>/createquestion/SA/', login_required(views.CreateSAQuestion.as_view()), name="createsaquestion"),
    path('rangemanagement/view/<rangeurl>/createquestion/OE/', login_required(views.CreateOEQuestion.as_view()), name="createoequestion"),
    path('rangemanagement/view/<rangeurl>/', login_required(views.RangeView.as_view()), name="rangeview"),
    path('rangemanagement/view/<rangeurl>/report/<username>/', login_required(views.ReportView.as_view()), name="reportview"),
    path('rangemanagement/view/<rangeurl>/report/<username>/mark/<questionid>/correct/', login_required(views.OEMarkCorrect.as_view()), name="reportview"),
    path('rangemanagement/view/<rangeurl>/report/<username>/mark/<questionid>/wrong/', login_required(views.OEMarkWrong.as_view()), name="reportview"),
    path('rangemanagement/view/<rangeurl>/remove/<username>/', login_required(views.RemoveStudentFromRange.as_view()), name="removestudentfromrange"),
    path('rangemanagement/view/<rangeurl>/removegroup/<groupname>/', login_required(views.RemoveGroupFromRange.as_view()), name="removegroupfromrange"),
    path('rangemanagement/view/<rangeurl>/archived/', login_required(views.ArchivedRangeQuestions.as_view()), name="archivedquestions"),
    path('rangemanagement/view/<rangeurl>/archived/unarchive/<questionid>/', login_required(views.UnarchiveQuestion.as_view()), name="unarchivequestions"),
    path('rangemanagement/view/<rangeurl>/archived/delete/<questionid>/', login_required(views.DeleteQuestionFromRange.as_view()), name="deletequestionfromrange"),
    path('rangemanagement/view/<rangeurl>/assignusers/', login_required(views.AssignUser.as_view()), name="assignuser"),
    path('rangemanagement/view/<rangeurl>/assigngroups/', login_required(views.AssignGroup.as_view()), name="assigngroup"),
    path('rangemanagement/view/<rangeurl>/assigngroups/add/<groupname>/', login_required(views.AddGroupRangeCart.as_view()), name="addgrouprangecart"),
    path('rangemanagement/view/<rangeurl>/assigngroups/remove/<groupname>/', login_required(views.RemoveGroupRangeCart.as_view()), name="removegrouprangecart"),
    path('rangemanagement/view/<rangeurl>/assigngroups/commit/', login_required(views.GroupRangeCommit.as_view()), name="grouprangecommit"),
    path('rangemanagement/view/<rangeurl>/assignusers/commit/', login_required(views.UserRangeCommit.as_view()), name="userrangecommit"),
    path('rangemanagement/view/<rangeurl>/assignusers/<username>/', login_required(views.AddUserRangeCart.as_view()), name="assignuser"),
    path('rangemanagement/view/<rangeurl>/assignusers/remove/<username>/', login_required(views.RemoveUserRangeCart.as_view()), name="removeusercart"),
    path('rangemanagement/view/<rangeurl>/edit/', login_required(views.ModifyRange.as_view()), name="modifyrange"),
    path('rangemanagement/view/<rangeurl>/activate/', login_required(views.ActivateRange.as_view()), name="activaterange"),
    path('rangemanagement/view/<rangeurl>/deactivate/', login_required(views.DeactivateRange.as_view()), name="deactivaterange"),
    path('rangemanagement/view/<rangeurl>/archive/<questionid>/', login_required(views.ArchiveQuestion.as_view()), name="archivequestion"),
    path('rangemanagement/view/<rangeurl>/import/', login_required(views.AddQuestioninRange.as_view()), name ='addquestionsinrange'),
    path('rangemanagement/view/<rangeurl>/import/commit/', login_required(views.AddQuestioninRangeCommit.as_view()), name ='addquestionsinrangecommit'),
    path('rangemanagement/view/<rangeurl>/import/add/<questionid>/', login_required(views.AddQuestionToCart.as_view()), name ='addquestiontocart'),
    path('rangemanagement/view/<rangeurl>/import/remove/<questionid>/', login_required(views.RemoveQuestionFromCart.as_view()), name ='removequestionfromcart'),
    path('rangemanagement/archive/<rangeurl>/', login_required(views.ArchiveRange.as_view()), name="archiverange"),
    path('rangemanagement/archived/', login_required(views.ArchivedRangeManagement.as_view()), name='archivedrangemanagement'),
    path('rangemanagement/archived/unarchive/<rangeurl>/', login_required(views.UnarchiveRange.as_view()), name='unarchiverange'),
    path('rangemanagement/archived/delete/<rangeurl>/', login_required(views.DeleteRange.as_view()), name='deleterange'),
    path('rangemanagement/view/<rangeurl>/edit/<questionid>/', login_required(views.EditQuestion.as_view()), name="editquestion"),
    path('rangemanagement/view/<rangeurl>/importcsv/', views.ImportCSV.as_view(), name='importcsv'),
    path('rangemanagement/view/<rangeurl>/exportcsv/', views.ExportCSV.as_view(), name='exportcsv'),
    path('rangemanagement/view/<rangeurl>/isopen/', views.IsOpen.as_view(), name='isopen'),
    path('rangemanagement/view/<rangeurl>/isclose/', views.IsClose.as_view(), name='isopen'),
    path('rangemanagement/view/<rangeurl>/csvtemplate/', views.DownloadCSVTemplate.as_view(), name='downloadcsvtemplate'),

    #QUESTION MANAGEMENT
    path('questionmanagement/', login_required(views.QuestionManagement.as_view()), name='questionmanagement'),
    path('questionmanagement/edit/<questionid>', login_required(views.EditQuestion.as_view()), name='editquestion'),
    path('questionmanagement/view/<questionid>', login_required(views.ViewQuestion.as_view()), name='viewquestion'),
    path('questionmanagement/archived', login_required(views.ArchivedQuestionManagement.as_view()), name='archivedquestionmanagement'),
    path('questionmanagement/archived/view/<questionid>', login_required(views.ViewQuestion.as_view()), name='unarchivefromquestionmanagement'),
    path('questionmanagement/archived/unarchive/<questionid>', login_required(views.UnarchiveFromQuestionManagement.as_view()), name='unarchivefromquestionmanagement'),
    path('<username>/changepassword', login_required(settingview.ResetPassword.as_view()), name='forcechangepassword'),

    #DOCKER MANAGEMENT
    path('dockermanagement/', login_required(views.DockerManagement.as_view()), name='dockermanagement'),
    path('dockermanagement/kill/<containername>/', login_required(views.AdminDockerKill.as_view()), name='killdocker'),

    #TEACHER MANAGEMENT
    path('teachermanagement/', views.TeacherView.as_view(), name='teacherview'),
    path('teachermanagement/addteacher/', views.AddTeacher.as_view(), name='addteacher'),

    #CLASS MANAGEMENT
    path('classmanagement/', views.ClassView.as_view(), name='classview'),
    path('classmanagement/addclass/', views.AddClass.as_view(), name='addclass'),

    path('SDLmanagement/', login_required(views.SDLManagement.as_view()), name='SDLManagement'),
    path('SDLmanagement/addpost/', login_required(views.AddPost.as_view()), name="addpost"),
    path('SDLmanagement/edit/<postid>/', login_required(views.EditPost.as_view()), name="editpost"),
    path('SDLmanagement/publish/<postid>/', login_required(views.PublishPost.as_view()), name="publishpost"),
    path('SDLmanagement/withdraw/<postid>/', login_required(views.WithdrawPost.as_view()), name="withdrawpost"),
    path('SDLmanagement/delete/<postid>/', login_required(views.DeletePost.as_view()), name="deletepost"),
    path('SDLmanagement/view/<postid>/', login_required(views.ViewPost.as_view()), name="viewpost"),
    path('SDLmanagement/view/<postid>/deletecomment/<commentid>', login_required(views.DeleteComment.as_view()), name="deletecomment"),
]  
