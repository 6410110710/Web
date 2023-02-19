from django.contrib import admin
from .models import Subject
from .models import MyWebUser
from .models import Event

#admin.site.register(Subject, SubjectAdmin)
admin.site.register(MyWebUser)
#admin.site.register(Event)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject_id', 'classroom')
    ordering = ('name',)
    search_fields = ('name', 'subject_id')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name','subject'), 'event_date', 'description', 'admin')
    list_display = ('name', 'event_date', 'subject')
    list_filter = ('event_date', 'subject')
    ordering = ('-event_date',)