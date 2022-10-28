from django.urls import path
from crewdashboard.views import add_new_locations, show_locations, show_json

app_name = 'crewdashboard'

urlpatterns = [
    path('dashboard/', show_locations, name='show_locations'),
    path('json/', show_json, name='json'),
    path('addlocation/', add_new_locations, name='addlocation'),
]