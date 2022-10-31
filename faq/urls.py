from django.urls import path
from .views import index, json, add, update_thumbsUp

app_name = 'faq'
urlpatterns = [
    path('', index, name='index'),
    path('json/', json, name='json'),
    path('add/', add, name='add'),
    path('thumbsup', update_thumbsUp, name='update_thumbsUp')
]