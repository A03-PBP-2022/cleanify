from banksampah.views import create_bank, show_bank, delete_bank
from django.urls import path

app_name = 'banksampah'

urlpatterns = [
    path('', create_bank, name='create'),
    path('show/', show_bank, name='show'),
    path('delete/<int:id>/', delete_bank, name='delete'),
]