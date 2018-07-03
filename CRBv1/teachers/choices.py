from django.utils.translation import gettext_lazy as _

DOCKER_CHOICES = (
    (1, _("YES")),
    (2, _("NO")),
)

FLAG = 'FL'
MCQ = 'MCQ'
SHORTANS = 'SA'
OPENENDED = 'OE'
TRUEFALSE = 'TF'
QUESTION_TYPE_CHOICES = (
    (FLAG, 'Flag'),
    (MCQ, 'Multiple Choice'),
    (SHORTANS, 'Short Answer'),
    (OPENENDED, 'Open Ended'),
    (TRUEFALSE, 'True/False')
)
