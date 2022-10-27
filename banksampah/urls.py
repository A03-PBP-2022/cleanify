from banksampah.views import create_post
from django.urls import path

app_name = 'banksampah'

urlpatterns = [
    path('', create_post, name='create_post'),
]