# core/user_urls.py
from django.urls import path
from .views import user_register, user_login

urlpatterns = [
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    # You can add more user-specific routes here in the future
]
