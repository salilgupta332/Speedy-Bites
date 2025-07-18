# core/user_urls.py
from django.urls import path
from .views import user_register, user_login
from . import views

urlpatterns = [
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
     path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('send-otp/', views.send_otp_view, name='send_otp'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    # You can add more user-specific routes here in the future
]
