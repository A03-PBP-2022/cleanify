from django.urls import path
from .views import index, json, add, update_thumbsUp,  Add_from_flutter

app_name = 'faq'
urlpatterns = [
    path('', index, name='index'),
    path('json/', json, name='json'),
    path('add/', add, name='add'),
    path('thumbsup/', update_thumbsUp, name='update_thumbsUp'),
    path('addFlutter/', Add_from_flutter, name ='Add_from_flutter')

]