from django.urls import path
from crewdashboard.views import add_new_locations, show_locations, show_json
from authc.views import logout_view
app_name = 'crewdashboard'

urlpatterns = [
    path('dashboard/', show_locations, name='show_locations'),
    path('json/', show_json, name='json'),
    path('', add_new_locations, name='addlocation'),
    path('logout/', logout_view, name='logout'),
]