from accounts.models import *
from ranges.models import *
import django_filters

class StudentFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    userclass__userclass = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'userclass__userclass', 'isaccepted']

class GroupFilter(django_filters.FilterSet):
    groupname = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Group
        fields = ['groupname']

class RangeFilter(django_filters.FilterSet):
    rangename = django_filters.CharFilter(lookup_expr='icontains')
    rangeurl = django_filters.CharFilter(lookup_expr='icontains')
    datecreated = django_filters.DateFilter()
    datestart = django_filters.DateFilter()
    dateend = django_filters.DateFilter()
    class Meta:
        model = Range
        fields = ['rangename', 'rangeurl', 'datecreated', 'datestart', 'dateend']

class QuestionFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    topicid__topicname = django_filters.CharFilter(lookup_expr='icontains')
    rangeid__rangeurl = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Questions
        fields = ['questiontype', 'topicid__topicname', 'title', 'rangeid__rangeactive', 'points', 'usedocker']
        

class TeacherFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = User
        fields = ['email', 'name', 'username']

class ClassFilter(django_filters.FilterSet):
    userclass = django_filters.CharFilter(lookup_expr='icontains')
    createdby__username = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = UserClass
        fields = ['userclass', 'createdby__username']