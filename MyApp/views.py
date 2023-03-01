from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Subject
from .forms import SubjectForm, EventForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.paginator import Paginator



def subject_text(request):
    response = HttpResponse(content_type='textplain')
    response['Content-Disposition'] = 'attachment; filename=subject.text'

    subjects = Subject.objects.all()

    lines = []
    # loop and Output
    for subject in subjects:
        lines.append(f'{subject.name}\n{subject.subject_id}\n{subject.classroom}\n\n')
    
    #Write text file
    response.writelines(lines)
    return response


def delete_subject(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    subject.delete()
    return redirect('list-subjects')

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('list-events')


def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True

    
    return render(request, 'event/add_event.html', {'form':form, 'submitted':submitted})

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    
    return render(request, 'event/update_event.html', {'event': event,'form':form})


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
    #subject_list = Subject.objects.all().order_by('name')
    subject_list = Subject.objects.all()

    #Set up Pagination
    p = Paginator(Subject.objects.all(), 2)
    page = request.GET.get('page')
    subjects = p.get_page(page)
    nums = "a" * subjects.paginator.num_pages
    return render(request, 'event/subject.html', {'subject_list': subject_list,'subjects': subjects, 'nums': nums})


def add_subject(request):
    submitted = False
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.owner = request.user.id #logged in user
            subject.save()
            #form.save()
            return HttpResponseRedirect('/add_subject?submitted=True')
    else:
        form = SubjectForm
        if 'submitted' in request.GET:
            submitted = True

    
    return render(request, 'event/add_subject.html', {'form':form, 'submitted':submitted})

def all_events(request):
    event_list = Event.objects.all().order_by('event_date')
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