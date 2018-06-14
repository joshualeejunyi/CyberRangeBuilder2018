from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.RangesView.as_view(), name="ranges"),
    path('<rangeurl>/play/', views.QuestionsView.as_view(), name="playrange"),
    path('<rangeurl>/play/Question<questionid>', views.AttemptQuestionView.as_view(), name="attemptquestion"),
    path('<rangeurl>/play/Question<questionid>/MCQ', views.AttemptMCQQuestionView.as_view(), name="attemptmcqquestion")
    # path('<rangename>/play/Question<questionid>', views.AttemptQuestionView.as_view(), name="attemptquestion")
]