from django.views import generic

from ranges.models import *

from accounts.models import User

from django.utils.dateparse import parse_date

import datetime

class ProgressView(generic.ListView):
    template_name='progress/progress.html'
    context_object_name = 'rangesobject'
    def get_queryset(self):
        user = self.request.user
        assignedranges = RangeStudents.objects.filter(studentID=user, rangeID__rangeactive=1).order_by('-lastaccess', '-dateJoined', '-pk')[:5]
        return assignedranges

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ProgressView, self).get_context_data(**kwargs)
        completedranges = RangeStudents.objects.filter(studentID=user).exclude(datecompleted=None)
        context['numberofcompletedranges'] = len(completedranges)
        empty = []
        empty2 = []
        rangenameslist = []
        percentlist = []
        if len(completedranges) != 0:
            # For the line graph
            pasttencompleted = completedranges.values_list('rangeID').order_by('-datecompleted')[:10]
            rangepoints = completedranges.values_list('points')

            totalpoints = 0
            for x in range(0, len(rangepoints)):
                totalpoints = totalpoints + rangepoints[x][0]
            
            rangemaxscores = 0
            x = 0
            for rangeobject in completedranges:
                rangemaxscores = rangemaxscores + rangeobject.rangeID.maxscore
                currentpoints = rangeobject.points
                currentmax = rangeobject.rangeID.maxscore
                percent = round(((currentpoints / currentmax) * 100), 2)
                x = x + 1
                if x < 6:
                    percentlist.append(percent)
                    rangenameslist.append(rangeobject.rangeID.rangename)

            averagepercent = round(totalpoints/rangemaxscores*100,2)
            context['averagepercent'] = averagepercent

        inactiveranges = RangeStudents.objects.filter(studentID=user, rangeID__rangeactive=False)

        topfive = 0
        for rangeobject in inactiveranges:
            ranking = RangeStudents.objects.filter(rangeID=rangeobject.rangeID.rangeid).order_by('-points')[:5]

            for students in ranking:
                if students.studentID == user:
                    topfive = topfive + 1

        context['topfive'] = topfive

        graphdata = str(list(zip(rangenameslist, percentlist)))
        graphdata = graphdata.replace("(", "[").replace(")", "]")
        context['graphdata'] = graphdata
        return context

class ReportView(generic.ListView):
    template_name='progress/report.html'
    context_object_name = 'questionsobject'
    def get_queryset(self):
        rangeurl = self.kwargs['rangeurl']
        username = self.request.user
        rangeid = Range.objects.filter(rangeurl=rangeurl).values_list('rangeid')[0][0]
        rangestudentobj = RangeStudents.objects.filter(studentID=username, rangeID__rangeid=rangeid)[0]

        studentquestionsobj = StudentQuestions.objects.filter(rangeid=rangeid, studentid=username)
        answeredquestionlist = []
        for question in studentquestionsobj:
            questionid = question.questionid.questionid
            if questionid not in answeredquestionlist:
                answeredquestionlist.append(questionid)

        questionsobj = Questions.objects.filter(rangeid=rangeid).exclude(questionid__in=answeredquestionlist)
        return questionsobj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rangeurl = self.kwargs['rangeurl']
        user = self.request.user
        rangeid = Range.objects.filter(rangeurl=rangeurl).values_list('rangeid')[0][0]

        rangeobj = Range.objects.get(rangeurl=rangeurl)
        rangestudentsobj = RangeStudents.objects.get(studentID=user, rangeID=rangeid)
        studentquestionsobj = StudentQuestions.objects.filter(studentid=user, rangeid=rangeid)
 
        context['rangename'] = rangeobj.rangename
        context['maxscore'] = rangeobj.maxscore
        pointsawarded = rangestudentsobj.points
        context['pointsawarded'] = pointsawarded

        hintpenaltyqueryset = StudentHints.objects.filter(studentid=user, rangeid = rangeid, hintactivated = True).values_list('questionid')
        totalhintpenalty = 0
        
        for x in range(0, len(hintpenaltyqueryset)):
            points = Questions.objects.filter(questionid = hintpenaltyqueryset[x][0]).values_list('hintpenalty')[0][0]
            totalhintpenalty = totalhintpenalty + int(points)

        context['hintpenalty'] = totalhintpenalty
        unobtained = rangeobj.maxscore - totalhintpenalty - pointsawarded
        context['unobtained'] = unobtained
        context['rangestudentsobj'] = rangestudentsobj
        context['studentquestionsobj'] = studentquestionsobj
        context['allquestions'] = Questions.objects.filter(rangeid=rangeid)
        context['rangeactive'] = Range.objects.filter(rangeid=rangeid).values_list('rangeactive')[0][0]
        rangeobject = Range.objects.get(rangeid=rangeid)
        dateend = rangeobject.dateend
        timeend = rangeobject.timeend
        
        canshowquestions = False
        
        if dateend is not None:
            if dateend >= datetime.date.today():
                currenttime = datetime.datetime.now().time()
                if currenttime >= timeend:
                    canshowquestions = True
        print(canshowquestions)
        context['canshowquestions'] = canshowquestions
        ranking = RangeStudents.objects.filter(rangeID=rangeid).order_by('-points')
        context['username'] = user
        context['ranking'] = ranking

        return context
