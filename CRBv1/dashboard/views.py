from django.views import generic
from ranges.models import RangeStudents, StudentQuestions, Range
from accounts.models import User
from ranges.views import Housekeeping

class DashboardView(generic.ListView):
    template_name='dashboard/dashboard.html'
    context_object_name = 'assignedranges'

    def get_queryset(self):
        user = self.request.user
        assignedranges = RangeStudents.objects.filter(studentID=user, rangeID__rangeactive=1).order_by('-lastaccess', '-dateJoined', '-pk')[:5]
        self.reportboxes = assignedranges[:4]
        latestfive = assignedranges[:5]
        currentranges = RangeStudents.objects.filter(studentID = user).values_list('rangeID')
        Housekeeping.get(self, currentranges)
        return latestfive

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        username = self.request.user
        
        latestrange = RangeStudents.objects.filter(studentID = username).order_by('-lastaccess', '-dateJoined')
        context['scoreboard'] = False
        if len(latestrange) != 0:
            context['scoreboard'] = True
            lateststudentrange = latestrange[0]
            latestrangeid = lateststudentrange.rangeID
            ranking = RangeStudents.objects.filter(rangeID=latestrangeid.rangeid).order_by('-points')
            context['rangeurl'] = Range.objects.filter(rangeid=latestrangeid.rangeid).values_list('rangeurl')[0][0]
            context['username'] = username
            context['rangename'] = latestrangeid.rangename
            context['maxscore'] = latestrangeid.maxscore
            context['userscore'] = lateststudentrange.points
            context['topfive'] = ranking[:5]
            # need to check if user in top 5 already
            intopfive = False
            for students in ranking[:5]:
                if students.studentID == username:
                    intopfive = True

            context['madeit'] = intopfive
            context['ranking'] = ranking
            context['reportboxes'] = self.reportboxes
        context['latestranges'] = latestrange
        if len(self.reportboxes) == 0:
            context['norange'] = True

        return context