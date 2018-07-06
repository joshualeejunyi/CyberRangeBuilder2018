from django.views import generic
from ranges.models import RangeStudents, StudentQuestions, Range
from accounts.models import User

class DashboardView(generic.ListView):
    template_name='dashboard/dashboard.html'
    context_object_name = 'assigned_ranges'

    def get_queryset(self):
        user = self.request.user
        currentranges = RangeStudents.objects.filter(studentID=user, datecompleted=None).values_list('rangeID',flat=True).order_by('-lastaccess')

        activerangesid = Range.objects.filter(rangeactive='1').values_list('rangeid', flat=True)
        activerangesid = list(activerangesid)

        finalrangelist = []
        for x in currentranges:
            if x in activerangesid:
                finalrangelist.append(x)
            if len(finalrangelist)==5:
                break

        assignedranges = Range.objects.none()
        for x in finalrangelist:
            rangename = Range.objects.filter(rangeid=x, rangeactive='1')
            assignedranges = assignedranges | rangename
        return assignedranges

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

            top_points = RangeStudents.objects.filter(rangeID=latestrange[0]).exclude(datecompleted=None).order_by('-points').values_list('points', flat=True)
            rankings = list(top_points)[:5]
            context['rankings'] = list(rankings)

            context['currentusername'] = user

            rankingnames = RangeStudents.objects.order_by('-points').filter(rangeID=latestrange[0]).values_list('studentID', flat=True)[:5]
            result = User.objects.filter(email=(rankingnames[0]))
            for x in range(len(rankingnames)):
                rankingusers= User.objects.filter(email=(rankingnames[x]))
                result = result | rankingusers

            for x in rankingnames:
                userrankings.append(result.get(email=x))
            context['zipranks'] = zip(rankings, userrankings)

            latest4id = list(reversed(RangeStudents.objects.filter(studentID=user, datecompleted__isnull=False).order_by('datecompleted').values_list('rangeID',flat=True)))

            finalpointslist = []
            finalnamelist = []
            finalmaxlist = []

            for x in latest4id:
                finalpointslist.append(RangeStudents.objects.filter(studentID=user, rangeID=x).order_by('datecompleted').values_list('points')[0][0])
                if len(finalpointslist) == 4:
                    break

            for x in latest4id:
                finalname = Range.objects.filter(rangeid=x).values_list('rangename')[0][0]
                finalnamelist.append(finalname)
                if len(finalnamelist) == 4:
                    break

            for x in latest4id:
                finalmaxlist.append(Range.objects.filter(rangeid=x).values_list('maxscore')[0][0])
                if len(finalmaxlist) == 4:
                    break

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

            print(finalnamelist)
            print(finalpointslist)
            print(finalmaxlist)
            context['zip4ranges'] = zip(finalnamelist, finalpointslist, finalmaxlist, listofrangelength)
            context['lengthofranges'] = len(finalnamelist)


        return context