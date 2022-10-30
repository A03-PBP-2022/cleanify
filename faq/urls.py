from django.urls import path
from .views import faq_index, faq_json, faq_add, faq_update_thumbsUp

app_name = 'faq'
urlpatterns = [
    path('', faq_index, name='faq_index'),
    path('json/', faq_json, name='faq_json'),
    path('add/', faq_add, name='faq_add'),
    path('thumbsup', faq_update_thumbsUp, name='faq_update_thumbsUp')
]