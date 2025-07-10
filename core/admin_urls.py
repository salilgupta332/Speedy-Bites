from django.urls import path
from . import views


urlpatterns = [
    path('admin-register/', views.admin_register, name='admin_register'),
    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
]