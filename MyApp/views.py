from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Subject
from .forms import SubjectForm, EventForm, EventFormAdmin
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages


def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me) 
        return render(request, 'event/my_events.html', {"events":events})
    else:
        messages.success(request, ("You Aren't Authorize To Veiw This Page!!"))
        return redirect('home')

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
    if request.user == event.admin:
        event.delete()
        messages.success(request, ("Event Deleted!!"))
        return redirect('list-events')
    else:
        messages.success(request, ("You Aren't Authorize To Delete This Event!!"))
        return redirect('list-events')


def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            
            if form.is_valid():
                event = form.save(commit=False)
                event.admin = request.user #logged in user
                event.save()
                #form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        #just going to page ,not submitting
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True

    
    return render(request, 'event/add_event.html', {'form':form, 'submitted':submitted})

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
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