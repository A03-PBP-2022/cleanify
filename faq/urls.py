from django.urls import path
from .views import faq_index, faq_json, faq_add, faq_update_thumbsUp

app_name = 'faq'
urlpatterns = [
    path('', faq_index, name='faq_index'),
    path('faq_json/', faq_json, name='faq_json'),
    path('faq_add/', faq_add, name='faq_add'),
    path('faq_update_thumbsUp/<int:id>', faq_update_thumbsUp)
]