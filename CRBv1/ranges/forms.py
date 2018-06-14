from django import forms
from .models import *

class AnswerForm(forms.ModelForm):
    answergiven = forms.CharField(label='Answer', max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    # def __init__(self, *args, **kwargs):
    #     questiontype = kwargs.pop('extra')
    #     super(UserCreationForm, self).__init__(*args, **kwargs)
    #     for i, question in enumerate(extra):
    #         self.fields['custom_%s' % i] = forms.CharField(label=question)

    def checkAnswer(self, user, answergiven, questioninstance, rangeinstance, questionid):
        marks = Questions.objects.filter(questionid = questionid).values_list('marks')[0][0]
        #print("MARKKKKKK ->>>>>>>" + str(marks))
        correctanswer = RangeQuestions.objects.filter(questionid = questionid).values_list('answer')[0][0]

        repeatedcheck = StudentQuestions.objects.filter(questionid = questionid, studentid = user, rangeid = rangeinstance)
        if len(repeatedcheck) == 0:
            check = False
            if answergiven.lower() == correctanswer.lower():
                check = True

            studentobject = StudentQuestions()
            studentobject.studentid = user
            studentobject.rangeid = rangeinstance
            studentobject.questionid = questioninstance
            studentobject.answergiven = answergiven
            studentobject.answercorrect = check
            studentobject.marksawarded = marks
            studentobject.save()

            if check is True:
                pointsobject = RangeStudents.objects.get(rangeID = rangeinstance, studentID = user)
                pointsobject.points += marks
                pointsobject.save()
            
                return True

        else:
            return False

    class Meta:
        model = StudentQuestions
        fields = ('answergiven',)

class AnswerMCQForm(forms.ModelForm):
    answergiven = forms.ChoiceField(label='Answer', widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices', None)
        #print(self.questionid)
        super(AnswerMCQForm, self).__init__(*args, **kwargs)
        self.fields['answergiven'].choices = self.choices

    def checkAnswer(self, user, answergiven, questioninstance, rangeinstance, questionid):
        marks = Questions.objects.filter(questionid = questionid).values_list('marks')[0][0]
        #print("MARKKKKKK ->>>>>>>" + str(marks))
        correctanswer = Questions.objects.filter(questionid = questionid).values_list('answer')[0][0]

        repeatedcheck = StudentQuestions.objects.filter(questionid = questionid, studentid = user, rangeid = rangeinstance)
        if len(repeatedcheck) == 0:
            check = False
            print(answergiven.lower())
            print(correctanswer.lower())
            if answergiven.lower() == correctanswer.lower():
                check = True

            studentobject = StudentQuestions()
            studentobject.studentid = user
            studentobject.rangeid = rangeinstance
            studentobject.questionid = questioninstance
            studentobject.answergiven = answergiven
            studentobject.answercorrect = check
            studentobject.marksawarded = marks
            studentobject.save()

            if check is True:
                pointsobject = RangeStudents.objects.get(rangeID = rangeinstance, studentID = user)
                pointsobject.points += marks
                pointsobject.save()
            
                return True

        else:
            return False


    class Meta:
        model = StudentQuestions
        fields = ('answergiven',)