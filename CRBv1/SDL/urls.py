from django.urls import path, include
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.SDLView.as_view(), name="SDL"),
    path('view/<postid>', (views.ViewPost.as_view()), name="viewpost"),
    path('view/deletecomment/<commentid>', (views.DeleteComment.as_view()), name="deletecomment"),
]
