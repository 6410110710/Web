from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Subject
from .forms import SubjectForm
from django.http import HttpResponseRedirect


def update_subject(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    form = SubjectForm(request.POST or None, instance=subject)
    if form.is_valid():
        form.save()
        return redirect('list-subjects')
    
    return render(request, 'event/update_subject.html', {'subject': subject,'form':form})

def search_subjects(request):
    if request.method == "POST":
        searched = request.POST['searched']
        subjects = Subject.objects.filter(name__contains=searched)
        return render(request, 'event/search_subjects.html', {'searched':searched, 'subjects':subjects})
    else:
        return render(request, 'event/search_subjects.html', {})


def show_subject(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    return render(request, 'event/show_subject.html', {'subject': subject})


def list_subject(request):
    subject_list = Subject.objects.all()
    return render(request, 'event/subject.html', {'subject_list': subject_list})


def add_subject(request):
    submitted = False
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_subject?submitted=True')
    else:
        form = SubjectForm
        if 'submitted' in request.GET:
            submitted = True

    
    return render(request, 'event/add_subject.html', {'form':form, 'submitted':submitted})

def all_events(request):
    event_list = Event.objects.all()
    return render(request, 'event/event_list.html', {'event_list': event_list})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "It's me"
    month = month.title()
    #convert month from name to num
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    #create calender
    cal = HTMLCalendar().formatmonth(year, month_number)
    #Get current year
    now = datetime.now()
    current_year = now.year
    #Get current time
    time = now.strftime('%H:%M:%S %p')

    return render(request, 'event/home.html', {
        "name" : name,
        "year" : year,
        "month" : month,
        "month_number" : month_number, 
        "cal" : cal,
        "current_year" : current_year,
        "time" : time,
    })