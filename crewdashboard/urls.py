from django.urls import path
from crewdashboard.views import add_new_locations, show_locations, show_json, delete_card, flutter_showJson, flutter_addLocation
app_name = 'crewdashboard'

urlpatterns = [
    path('', add_new_locations, name='addlocation'),
    path('dashboard/', show_locations, name='show_locations'),
    path('dashboard/', show_locations, name='show_locations_admin'),
    path('json/', show_json, name='json'),
    path('delete/', delete_card, name='delete_card'),
    path('reportlocation/', flutter_addLocation, name='addlocationflutter'),
    path('locations/', flutter_showJson, name='jsonflutter')
]
