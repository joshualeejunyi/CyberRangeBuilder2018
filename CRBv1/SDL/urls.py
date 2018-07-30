from django.urls import path, include
from django.conf.urls import url

from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(views.SDLView.as_view()), name="SDL"),
    path('view/<postid>', login_required(views.ViewPost.as_view()), name="viewpost"),
    path('view/deletecomment/<commentid>', login_required(views.DeleteComment.as_view()), name="deletecomment"),
]
