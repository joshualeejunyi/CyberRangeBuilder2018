from django.views import generic
from ranges.models import RangeStudents, StudentQuestions, Range
from accounts.models import User

class DashboardView(generic.ListView):
    template_name='dashboard/dashboard.html'
    context_object_name = 'assigned_ranges'

    def get_queryset(self):
        user = self.request.user
        currentranges = RangeStudents.objects.filter(studentID=user, datecompleted=None).values_list('rangeID').order_by('-lastaccess')[:5]
        emptylist = []
        for x in range(0, len(currentranges)):
            emptylist.append(currentranges[x][0])
        if len(currentranges) != 0:
            result = Range.objects.filter(rangeid=(currentranges[0][0]))
            for x in range(1, len(currentranges)):
                assignedranges= Range.objects.filter(rangeid=(currentranges[x][0]))
                result = result | assignedranges
        else:
            return None
        finalist = []
        for x in emptylist:
            finalist.append(result.get(rangeid=x))
        return finalist

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(DashboardView, self).get_context_data(**kwargs)
        completedrange = RangeStudents.objects.filter(studentID=user, datecompleted__isnull=False).values_list('rangeID')
        userrankings = []
        if completedrange:
            latestrange = RangeStudents.objects.filter(studentID=user).values_list('rangeID').latest('datecompleted')
            context['latest_range'] = latestrange

            latestrangename = Range.objects.filter(rangeid=latestrange[0]).values_list('rangename')
            context['range_name'] = latestrangename[0][0]

            context['max_score'] = Range.objects.filter(rangeid=latestrange[0]).values_list('maxscore', flat=True)[0]

            total_score = RangeStudents.objects.filter(studentID=user).values_list('points').latest('datecompleted')
            context['total_score'] = total_score[0]

            top_points = RangeStudents.objects.filter(rangeID=2).order_by('-points').values_list('points', flat=True)
            rankings = list(top_points)[:5]
            context['rankings'] = list(rankings)

            context['currentusername'] = user

            rankingnames = RangeStudents.objects.order_by('-points').filter(rangeID=latestrange[0]).values_list('studentID', flat=True)[:5]
            result = User.objects.filter(email=(rankingnames[0]))
            print(rankingnames)
            for x in range(len(rankingnames)):
                rankingusers= User.objects.filter(email=(rankingnames[x]))
                result = result | rankingusers

            for x in rankingnames:
                userrankings.append(result.get(email=x))
                print(userrankings)
            context['zipranks'] = zip(rankings, userrankings)

            latest4points = RangeStudents.objects.filter(studentID=user, datecompleted__isnull=False).order_by('datecompleted')[:4].values_list('points', flat=True)
            latestpoints= list(reversed(latest4points))

            latest4id = RangeStudents.objects.filter(studentID=user, datecompleted__isnull=False).order_by('datecompleted')[:4].values_list('rangeID')
            latest4id = list(reversed(latest4id))
            empty = []
            for x in range(0, len(latest4id)):
                empty.append(latest4id[x][0])
            if len(latest4id) !=0:
                result = Range.objects.filter(rangeid=(latest4id[0][0]))
                for x in range(1, len(latest4id)):
                    latest4Rid = Range.objects.filter(rangeid=(latest4id[x][0]))
                    result = result | latest4Rid
            finalnamelist = []
            for x in empty:
                finalnamelist.append(result.filter(rangeid=x).values_list('rangename')[0][0])

            finalmaxlist = []
            for x in empty:
                finalmaxlist.append(result.filter(rangeid=x).values_list('maxscore')[0][0])

            listofrangelength = range(1, (len(finalnamelist)+1))

            if user not in userrankings:
                context['userintop5'] = False
                userscore = RangeStudents.objects.filter(studentID=user, rangeID=latestrange[0]).values_list('points')
                context['userscore'] = userscore[0][0]
                usernumbers = list(reversed(RangeStudents.objects.filter(rangeID=latestrange[0]).values_list('points', flat=True).order_by('points')))
                userrank = usernumbers.index(userscore[0][0])
                context['userrank'] = userrank+1
            else:
                context['userintop5'] = True

            context['zip4ranges'] = zip(finalnamelist, latestpoints, finalmaxlist, listofrangelength)
            context['lengthofranges'] = len(finalnamelist)


        return context