from django.views import generic

from ranges.models import *

from accounts.models import User

from django.utils.dateparse import parse_date

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
        if len(completedranges) != 0:
            # For the line graph
            pasttencompleted = completedranges.values_list('rangeID').order_by('-datecompleted')[:10]
            rangepoints = completedranges.values_list('points')

            totalpoints = 0
            for x in range(0, len(rangepoints)):
                totalpoints = totalpoints + rangepoints[x][0]
            
            rangemaxscores = 0
            percentlist = []
            rangenameslist = []
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

        
        print('------------------------------')
        print(graphdata)
        print('------------------------------')

            
            


            #userpastcompletedrangesscore = list(reversed(RangeStudents.objects.filter(studentID=user).order_by('-datecompleted').exclude(datecompleted=None).values_list('points', flat=True)[:10]))

            #pastcompletedrangenames = []
            # for x in pastcompletedrangesid:
            #     rangename = Range.objects.filter(rangeid=x).values_list('rangename', flat=True)
            #     datecomplete = RangeStudents.objects.filter(rangeID=x,studentID=user).values_list('datecompleted')
            #     datecompleted = str(datecomplete[0][0])
            #     datecompleted = datecompleted[0:10]
            #     datecompleted = parse_date(datecompleted)
            #     rangenamedate = str(rangename[0]+" ("+str(datecompleted)+")")
            #     pastcompletedrangenames.append(str(rangenamedate))

            # for x in range(0, len(pastcompletedrangesid)):
            #     empty2.append(pastcompletedrangesid[x])
            # if len(pastcompletedrangesid) != 0:
            #     rangescore = Range.objects.filter(rangeid=(pastcompletedrangesid[0])).values_list('maxscore',flat=True)
            #     for x in range(1, len(pastcompletedrangesid)):
            #         pastcompletedrangescore = Range.objects.filter(rangeid=(pastcompletedrangesid[x])).values_list('maxscore',flat=True)
            #         rangescore = rangescore | pastcompletedrangescore
            # pastcompletedrangescores = []
            # for x in pastcompletedrangesid:
            #     pastcompletedrangescores.append(rangescore.get(rangeid=x))

            # percentlist = []
            # for x in range(0, len(pastcompletedrangesid)):
            #     percent = round(((userpastcompletedrangesscore[x] / pastcompletedrangescores[x]) * 100), 2)
            #     percentlist.append(percent)
            # percentlist = list(map(float, percentlist))

            # finallinegraphdata = str(list(zip(pastcompletedrangenames, percentlist)))
            # finallinegraphdata = finallinegraphdata.replace("(", "[").replace(")", "]")
            # context['linegraphdata'] = finallinegraphdata

            # # For achievements
            # context['useraveragescore'] = round((sum(map(float, percentlist)) / len(pastcompletedrangesid)),2)

            # rankingusernames = []
            # completedranges = RangeStudents.objects.filter(studentID=user).exclude(datecompleted=None).values_list('rangeID')

            # for x in completedranges:
            #     rankings = RangeStudents.objects.filter(rangeID=x).values_list('studentID',flat=True).order_by('-points')[:5]
            #     for y in rankings:
            #         top5rankings = User.objects.filter(email=y).values_list('username',flat=True)
            #         rankingusernames.append(top5rankings[0])

            # context['frequencyoftop5'] = rankingusernames.count(str(user))

            # # For the table
            # allrangenames = []
            # allrangescores = []
            # alluserscores = []
            # allrangeurls = []
            # completedrangeslist = list(reversed(RangeStudents.objects.filter(studentID=user).exclude(datecompleted=None).values_list('rangeID',flat=True).order_by('datecompleted')))

            # for x in completedrangeslist:
            #     allrangename = Range.objects.filter(rangeid=x).values_list('rangename', flat=True)[0]
            #     allrangenames.append(allrangename)

            # for x in completedrangeslist:
            #     alluserscore = RangeStudents.objects.filter(rangeID=x,studentID=user).values_list('points', flat=True)[0]
            #     alluserscores.append(alluserscore)

            # for x in completedrangeslist:
            #     allrangescore = Range.objects.filter(rangeid=x).values_list('maxscore', flat=True)[0]
            #     allrangescores.append(allrangescore)

            # for x in completedrangeslist:
            #     allrangeurl = Range.objects.filter(rangeid=x).values_list('rangeurl', flat=True)[0]
            #     allrangeurls.append(allrangeurl)

            # context['rangetabledata'] = zip(allrangenames, alluserscores, allrangescores, allrangeurls)

        return context

class ReportView(generic.ListView):
    template_name='progress/report.html'
    context_object_name = 'rangereport'
    def get_queryset(self):
        rangeurl = self.kwargs['rangeurl']
        completedrange = Range.objects.filter(rangeurl=rangeurl)

        return completedrange

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rangeurl = self.kwargs['rangeurl']
        user = self.request.user
        completedrange = Range.objects.filter(rangeurl=rangeurl).values_list('rangeid')[0][0]

        latestrange = RangeStudents.objects.filter(studentID=user, rangeID=completedrange).values_list('rangeID', flat=True)
        context['latest_range'] = latestrange

        latestrangename = Range.objects.filter(rangeid=latestrange[0]).values_list('rangename')
        context['range_name'] = latestrangename[0][0]

        context['max_score'] = Range.objects.filter(rangeid=latestrange[0]).values_list('maxscore', flat=True)[0]

        total_score = RangeStudents.objects.filter(studentID=user).values_list('points').latest('datecompleted')
        context['total_score'] = total_score[0]

        # For Question Report
        questionidlist = Questions.objects.filter(rangeid=completedrange).values_list('questionid', flat=True)

        questiontitles=[]
        questiontexts=[]
        useranswers=[]
        questionanswers=[]
        usermarks=[]
        questionmarks=[]
        topicids = []
        topics = []

        for x in questionidlist:
            questiontitle = Questions.objects.filter(questionid=x).values_list('title')[0][0]
            questiontitles.append(questiontitle)

        for x in questionidlist:
            questiontext = Questions.objects.filter(questionid=x).values_list('text')[0][0]
            questiontexts.append(questiontext)

        for x in questionidlist:
            useranswer = StudentQuestions.objects.filter(questionid=x, rangeid=completedrange, studentid=user).values_list('answergiven')[0][0]
            useranswers.append(useranswer)

        for x in questionidlist:
            questionanswer = Questions.objects.filter(questionid=x, rangeid=completedrange).values_list('answer')[0][0]
            questionanswers.append(questionanswer)

        for x in questionidlist:
            usermark = StudentQuestions.objects.filter(questionid=x, rangeid=completedrange, studentid=user).values_list('marksawarded')[0][0]
            usermarks.append(usermark)

        for x in questionidlist:
            questionmark = Questions.objects.filter(questionid=x).values_list('points')[0][0]
            questionmarks.append(questionmark)

        for x in questionidlist:
            topicid = Questions.objects.filter(questionid=x).values_list('topicid')[0][0]
            topicids.append(topicid)

        for x in topicids:
            topic = QuestionTopic.objects.filter(topicid=x).values_list('topicname')[0][0]
            topics.append(topic)

        context['reportdata'] = zip(questiontitles, questiontexts, useranswers, questionanswers, usermarks, questionmarks, topics)

        return context