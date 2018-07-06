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

    class Meta:
        model = Range
        fields = ['rangename', 'datecreated', 'datestart', 'timestart', 'dateend', 'timeend', 'maxscore', 'rangecode']

class QuestionFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='istartswith')
    typicid__topicname = django_filters.CharFilter(lookup_expr='istartswith')
    class Meta:
        model = Questions
        fields = ['questiontype', 'topicid__topicname', 'title']