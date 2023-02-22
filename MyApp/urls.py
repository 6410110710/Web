
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('<int:year>/<str:month>', views.home, name="home"),
    path('events', views.all_events, name="list-events"),
    path('add_subject', views.add_subject, name="add-subject"),
    path('list_subject', views.list_subject, name="list-subjects"),
    path('show_subject/<subject_id>', views.show_subject, name='show-subject'),
    path('search_subjects', views.search_subjects, name='search-subjects'),
    path('update_subject/<subject_id>', views.update_subject, name='update-subject'),
    path('add_event', views.add_event, name="add-event"),
    path('update_event/<event_id>', views.update_event, name='update-event'),
    path('delete_event/<event_id>', views.delete_event, name='delete-event'),
    path('delete_subject/<subject_id>', views.delete_subject, name='delete-subject'),

    ]   
