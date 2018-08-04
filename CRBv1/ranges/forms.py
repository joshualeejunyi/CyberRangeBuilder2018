from django import forms
from .models import *
from django.utils import timezone

class AnswerForm(forms.ModelForm):
    answergiven = forms.CharField(label='Answer', widget=forms.TextInput(attrs={'class' : 'form-control'}))

    def checkAnswer(self, user, answergiven, questioninstance, rangeinstance, questionid):
        points = Questions.objects.filter(questionid = questionid).values_list('points')[0][0]
        hintactivated = StudentHints.objects.filter(studentid = user, rangeid = rangeinstance, questionid = questioninstance).values_list('hintactivated')
        if len(hintactivated) != 0:
            points = points - int(Questions.objects.filter(questionid = questionid).values_list('hintpenalty')[0][0])

        correctanswer = Questions.objects.filter(questionid = questionid).values_list('answer')[0][0]
        isthisashortanswer = Questions.objects.filter(questionid = questionid).values_list('questiontype')[0][0]
        repeatedcheck = StudentQuestions.objects.filter(questionid = questionid, studentid = user, rangeid = rangeinstance).count()
        numberofrangequestions = Questions.objects.filter(rangeid=rangeinstance, isarchived=False).count()
        

        check = False
        if isthisashortanswer == 'SA':
            saanswer = correctanswer.lower().split()
            saanswerset = set(saanswer)
            givenanswer = answergiven.lower().split()
            givenanswerset = set(givenanswer)
            
            keywords = len(saanswer)
            distributedpoints = float(points)/float(keywords)
            
            setdifference = saanswerset.symmetric_difference(givenanswerset)
            diffcount = len(setdifference)

            if diffcount == 0:
                check = True
            else:
                points = points - (distributedpoints * diffcount)

        elif isthisashortanswer == 'OE':
            check = False
        else:
            if answergiven.lower() == correctanswer.lower():
                check = True

        studentobject = StudentQuestions()
        studentobject.studentid = user
        studentobject.rangeid = rangeinstance
        studentobject.questionid = questioninstance
        studentobject.answergiven = answergiven
        studentobject.answercorrect = check
        studentobject.attempts = repeatedcheck + 1

        if check is True:
            studentobject.marksawarded = points
            pointsobject = RangeStudents.objects.get(rangeID = rangeinstance, studentID = user)

            if repeatedcheck != 0:
                if isthisashortanswer == 'SA':
                    previousanswerobject = StudentQuestions.objects.get(rangeid = rangeinstance, questionid = questioninstance, studentid = user, attempts = repeatedcheck)
                    pointsobject.points = pointsobject.points - previousanswerobject.marksawarded
                
            pointsobject.points += points
            checkcompletion = len(StudentQuestions.objects.filter(rangeid = rangeinstance, studentid = user, answercorrect = 1))

            if checkcompletion == numberofrangequestions:
                pointsobject.datecompleted = timezone.now()

            studentobject.save()
            pointsobject.save()
        
            return True
        else:

            pointsobject = RangeStudents.objects.get(rangeID = rangeinstance, studentID = user)
            
            if isthisashortanswer == 'SA':
                if repeatedcheck != 0:
                    previousanswerobject = StudentQuestions.objects.get(rangeid = rangeinstance, questionid = questioninstance, studentid = user, attempts = repeatedcheck)
                    pointsobject.points = pointsobject.points - previousanswerobject.marksawarded
                
                pointsobject.points += points
                studentobject.marksawarded = points
            else:
                studentobject.marksawarded = 0

            pointsobject.save()
            studentobject.save()

    class Meta:
        model = StudentQuestions
        fields = ('answergiven',)

class AnswerMCQForm(forms.ModelForm):
    answergiven = forms.ChoiceField(label='Answer', widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices', None)
        super(AnswerMCQForm, self).__init__(*args, **kwargs)
        self.fields['answergiven'].choices = self.choices

    def checkAnswer(self, user, answergiven, questioninstance, rangeinstance, questionid):
        points = Questions.objects.filter(questionid = questionid).values_list('points')[0][0]
        hintactivated = StudentHints.objects.filter(studentid = user, rangeid = rangeinstance, questionid = questioninstance).values_list('hintactivated')
        if len(hintactivated) != 0:
            points = points - int(Questions.objects.filter(questionid = questionid).values_list('hintpenalty')[0][0])

        correctanswer = Questions.objects.filter(questionid = questionid).values_list('answer')[0][0]
        repeatedcheck = StudentQuestions.objects.filter(questionid = questionid, studentid = user, rangeid = rangeinstance).count()
        numberofrangequestions = Questions.objects.filter(rangeid=rangeinstance, isarchived=False).count()

        check = False
        if answergiven.lower() == correctanswer.lower():
            check = True

        studentobject = StudentQuestions()
        studentobject.studentid = user
        studentobject.rangeid = rangeinstance
        studentobject.questionid = questioninstance
        studentobject.answergiven = answergiven
        studentobject.answercorrect = check
        studentobject.attempts = repeatedcheck+ 1

        if check is True:
            studentobject.marksawarded = points
            pointsobject = RangeStudents.objects.get(rangeID = rangeinstance, studentID = user)
            pointsobject.points += points

            checkcompletion = len(StudentQuestions.objects.filter(rangeid = rangeinstance, studentid = user, answercorrect = 1))

            if checkcompletion == numberofrangequestions:
                pointsobject.datecompleted = timezone.now()

            studentobject.save()
            pointsobject.save()
        
            return True
        else:
            studentobject.marksawarded = 0
            studentobject.save()

    class Meta:
        model = StudentQuestions
        fields = ('answergiven',)