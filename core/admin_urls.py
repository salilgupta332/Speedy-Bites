from django.urls import path , include
from . import views


urlpatterns = [
    path('admin-register/', views.admin_register, name='admin_register'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/Menu-dashboard/', views.menu_dashboard, name='menu_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    
]