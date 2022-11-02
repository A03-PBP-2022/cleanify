from django.urls import path
from crewdashboard.views import add_new_locations, show_locations, show_json, delete_card
app_name = 'crewdashboard'

urlpatterns = [
    path('dashboard/', show_locations, name='show_locations'),
    path('json/', show_json, name='json'),
    path('', add_new_locations, name='addlocation'),
    path('delete/', delete_card, name='delete_card'),
]