from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(views.RangesView.as_view()), name="ranges"),
    path('<rangeurl>/play/', login_required(views.QuestionsView.as_view()), name="playrange"),
    path('<rangeurl>/play/Question<questionid>', login_required(views.AttemptQuestionView.as_view()), name="attemptquestion"),
    path('<rangeurl>/play/Question<questionid>/MCQ', login_required(views.AttemptMCQQuestionView.as_view()), name="attemptmcqquestion"),
    path('entercode', login_required(views.EnterCode.as_view()), name="entercode"),
]