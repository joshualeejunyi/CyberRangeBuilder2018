from accounts.models import *
from ranges.models import *
import django_filters

class StudentFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='istartswith')
    name = django_filters.CharFilter(lookup_expr='istartswith')
    email = django_filters.CharFilter(lookup_expr='istartswith')
    userclass = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'userclass', 'isaccepted']

class GroupFilter(django_filters.FilterSet):
    groupname = django_filters.CharFilter(lookup_expr='istartswith')
    class Meta:
        model = Group
        fields = ['groupname']

class RangeFilter(django_filters.FilterSet):
    rangename = django_filters.CharFilter(lookup_expr='istartswith')
    rangeurl = django_filters.CharFilter(lookup_expr='istartswith')
    datecreated = django_filters.DateFilter()
    datestart = django_filters.DateFilter()
    dateend = django_filters.DateFilter()
    class Meta:
        model = Range
        fields = ['rangename', 'rangeurl', 'datecreated', 'datestart', 'dateend']

class QuestionFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='istartswith')
    topicid__topicname = django_filters.CharFilter(lookup_expr='istartswith')
    
    class Meta:
        model = Questions
        fields = ['questiontype', 'topicid__topicname', 'title', 'rangeid__isdisabled']
        

class TeacherFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = User
        fields = ['email', 'name', 'username']

class BigQuestionFilter(django_filters.FilterSet):
    text = django_filters.CharFilter(lookup_expr='icontains')
    hint = django_filters.CharFilter(lookup_expr='icontains')
    answer = django_filters.CharFilter(lookup_expr='icontains')
    title = django_filters.CharFilter(lookup_expr='icontains')
    questiontype = django_filters.CharFilter(lookup_expr='icontains')
    topicid__topicname = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Questions
        fields = ['questiontype', 'text', 'hint','answer', 'title']