from banksampah.views import form_bank
from django.urls import path

app_name = 'banksampah'

urlpatterns = [
    path('', form_bank, name='form_bank'),
]