from banksampah.views import create_post, show_bank, delete_bank
from django.urls import path

app_name = 'banksampah'

urlpatterns = [
    path('', create_post, name='create_post'),
    path('show-bank/', show_bank, name='show_bank'),
    path('delete_task/<int:id>/', delete_bank, name='delete_bank'),
]