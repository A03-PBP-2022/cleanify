from django.urls import path
from crewdashboard import dashboard

app_name = 'crewdashboard'

urlpatterns = [
    path('dashboard/', show_locations, name='show_locations'),
]