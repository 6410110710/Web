from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    name = models.CharField("Subject Name",max_length=120) 
    subject_id = models.CharField(max_length=300)
    classroom = models.CharField(max_length=120)
    owner = models.IntegerField("Subject Owner", blank=False, default=1)
    def __str__(self):
        return self.name

class MyWebUser(models.Model):
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Event(models.Model):
    name = models.CharField(max_length=120)
    event_date = models.DateTimeField('date')
    subject = models.ForeignKey(Subject, blank=True, null=True, on_delete=models.CASCADE)
    #subject = models.CharField(max_length=120)
    admin = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyWebUser, blank=True)
    
    def __str__(self):
        return self.name