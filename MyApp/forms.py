from django import forms
from django.forms import ModelForm
from .models import Subject

#Create a subject form
class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ('name', 'subject_id', 'classroom')
        
