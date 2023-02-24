
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('MyApp.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
]

# Configure Admin Title
admin.site.site_header = "Administration Page"
admin.site.site_title = "My Web"
admin.site.index_title = ""