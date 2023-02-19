
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('<int:year>/<str:month>', views.home, name="home"),
    path('events', views.all_events, name="list-events"),
    path('add_subject', views.add_subject, name="add-subject"),
    path('list_subject', views.list_subject, name="list-subjects"),
    path('show_subject/<subject_id>', views.show_subject, name='show-subject'),
    

]   
