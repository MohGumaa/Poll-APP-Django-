from django import forms
from .models import Question

class UpdateQuestion(forms.ModelForm):
    class Meta:
        model = Question
        labels = {
        "question_text" :''
        }
        fields = ['question_text']
