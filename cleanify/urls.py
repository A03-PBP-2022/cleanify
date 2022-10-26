from django.urls import path
from cleanify.views import register
from cleanify.views import logout_user
from cleanify.views import login_user

app_name = 'cleanify'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]