from django import forms
from .models import *
from django.utils import timezone
import datetime

class AnswerForm(forms.ModelForm):
    answergiven = forms.CharField(label='Answer', max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    def checkAnswer(self, user, answergiven, questioninstance, rangeinstance, questionid):
        points = Questions.objects.filter(questionid = questionid).values_list('points')[0][0]
        hintactivated = StudentHints.objects.filter(studentid = user, rangeid = rangeinstance, questionid = questioninstance).values_list('hintactivated')
        if len(hintactivated) != 0:
            points = points - int(Questions.objects.filter(questionid = questionid).values_list('hintpenalty')[0][0])

        correctanswer = Questions.objects.filter(questionid = questionid).values_list('answer')[0][0]
        isthisashortanswer = Questions.objects.filter(questionid = questionid).values_list('questiontype')[0][0]
        repeatedcheck = StudentQuestions.objects.filter(questionid = questionid, studentid = user, rangeid = rangeinstance)
        numberofrangequestions = Questions.objects.filter(rangeid=rangeinstance).count()
        

        check = False
        if isthisashortanswer == 'SA':
            saanswer = correctanswer.lower().split()
            givenanswer = answergiven.lower().split()
            keywords = len(saanswer)
            keycheck = 0
            for x in saanswer:
                for y in givenanswer:
                    if y in x:
                        keycheck += 1
                        if keycheck == keywords:
                            check = True
        elif isthisashortanswer == 'OE':
            check = False
        else:
            if answergiven.lower() == correctanswer.lower():
                check = True

        if len(repeatedcheck) == 0:
            studentobject = StudentQuestions()
            studentobject.studentid = user
            studentobject.rangeid = rangeinstance
            studentobject.questionid = questioninstance
            studentobject.answergiven = answergiven
            studentobject.answercorrect = check

            if check is True:
                studentobject.marksawarded = points
                studentobject.save()

                pointsobject = RangeStudents.objects.get(rangeID = rangeinstance, studentID = user)
                pointsobject.points += points
                checkcompletion = len(StudentQuestions.objects.filter(rangeid = rangeinstance, studentid = user, answercorrect = 1))

                print(checkcompletion)
                print(numberofrangequestions)

                if checkcompletion == numberofrangequestions:
                    pointsobject.datecompleted = timezone.now()
                pointsobject.save()


                
            
                return True
            else:
                studentobject.marksawarded = 0
                studentobject.save()

        else:
            studentobject = StudentQuestions()
            studentobject.studentid = user
            studentobject.rangeid = rangeinstance
            studentobject.questionid = questioninstance
            studentobject.answergiven = answergiven
            studentobject.answercorrect = check
            studentobject.attempts = len(repeatedcheck) + 1

            if check is True:
                studentobject.marksawarded = points
                studentobject.save()

                pointsobject = RangeStudents.objects.get(rangeID = rangeinstance, studentID = user)
                pointsobject.points = pointsobject.points - studentobject.marksawarded
                pointsobject.points += points

                checkcompletion = len(StudentQuestions.objects.filter(rangeid = rangeinstance, studentid = user, answercorrect = 1))

                if checkcompletion == numberofrangequestions:
                    pointsobj.datecompleted = timezone.now()

                return True
            else:
                studentobject.marksawarded = 0
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
        isthisashortanswer = Questions.objects.filter(questionid = questionid).values_list('questiontype')[0][0]
        repeatedcheck = StudentQuestions.objects.filter(questionid = questionid, studentid = user, rangeid = rangeinstance)
        numberofrangequestions = Questions.objects.filter(rangeid=rangeinstance).count()

        check = False
        if isthisashortanswer == 'SA':
            saanswer = correctanswer.lower().split()
            givenanswer = answergiven.lower().split()
            keywords = len(saanswer)
            keycheck = 0
            for x in saanswer:
                for y in givenanswer:
                    if y in x:
                        keycheck += 1
                        if keycheck == keywords:
                            check = True
        elif isthisashortanswer == 'OE':
            check = False
        else:
            if answergiven.lower() == correctanswer.lower():
                check = True

        if len(repeatedcheck) == 0:
            studentobject = StudentQuestions()
            studentobject.studentid = user
            studentobject.rangeid = rangeinstance
            studentobject.questionid = questioninstance
            studentobject.answergiven = answergiven
            studentobject.answercorrect = check

            if check is True:
                studentobject.marksawarded = points
                studentobject.save()

                pointsobject = RangeStudents.objects.get(rangeID = rangeinstance, studentID = user)
                pointsobject.points += points
                checkcompletion = len(StudentQuestions.objects.filter(rangeid = rangeinstance, studentid = user, answercorrect = 1))

                if checkcompletion == numberofrangequestions:
                    pointsobject.datecompleted = timezone.now()

                pointsobject.save()

                return True
            else:
                studentobject.marksawarded = 0
                studentobject.save()

        else:
            studentobject = StudentQuestions()
            studentobject.studentid = user
            studentobject.rangeid = rangeinstance
            studentobject.questionid = questioninstance
            studentobject.answergiven = answergiven
            studentobject.answercorrect = check
            studentobject.answercorrect = check
            studentobject.attempts = len(repeatedcheck) + 1

            if check is True:
                studentobject.marksawarded = points
                studentobject.save()

                pointsobject = RangeStudents.objects.get(rangeID = rangeinstance, studentID = user)
                pointsobject.points = pointsobject.points - studentobject.marksawarded
                pointsobject.points += points
                pointsobject.save()

                checkcompletion = len(StudentQuestions.objects.filter(rangeid = rangeinstance, studentid = user, answercorrect = 1))

                if checkcompletion == numberofrangequestions:
                    pointsobject.datecompleted = timezone.now()

                return True
            else:
                studentobject.marksawarded = 0
                studentobject.save()

    class Meta:
        model = StudentQuestions
        fields = ('answergiven',)