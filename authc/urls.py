from django.urls import path
from .views import registration_view, login_view, logout_view, api_login, api_logout, api_perms

app_name = 'authc'

urlpatterns = [
    path('register/',registration_view, name='register'),
    path('login/',login_view, name='login'),
    path('logout/',logout_view, name='logout'),
    path('api/login', api_login, name='api_login'),
    path('api/logout', api_logout, name='api_logout'),
    path('api/register', api_register, name='api_register'),
    path('api/perms', api_perms, name='api_perms') 
]