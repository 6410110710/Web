from django import forms
from django.forms import ModelForm
from .models import Subject, Event

#Create a subject form
class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ('name', 'subject_id', 'classroom')
        labels = {
            'name': '',
            'subject_id': '',
            'classroom': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Subject Name'}), 
            'subject_id': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Subject ID'}),
            'classroom': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Classroom'}),
        }
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name','description', 'event_date', 'subject','attendees','admin')
        labels = {
            'name': '',
            'description': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'subject': 'Subject',
            'attendees': 'Attendees',
            'admin': 'Admin',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event Name'}), 
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Description'}),
            'event_date': forms.DateTimeInput(attrs={'class':'form-control', 'placeholder': 'Event Date'}),
            'subject': forms.Select(attrs={'class':'form-select', 'placeholder': 'Subject'}),
            'attendees': forms.SelectMultiple(attrs={'class':'form-select', 'placeholder': 'Attendees'}),
            'admin': forms.Select(attrs={'class':'form-select', 'placeholder': 'Admin'}),
        }
