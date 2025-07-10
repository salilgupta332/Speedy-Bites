# core/urls.py

from django.urls import path , include
from .views import home, landing_page, add_menu_item, edit_menu_item, delete_menu_item , admin_register
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('', landing_page, name='landing'),                     # Landing page
    path('menu/', home, name='home'),                           # Admin dashboard
    path('add/', add_menu_item, name='add_menu_item'),
    path('edit/<str:item_id>/', edit_menu_item, name='edit_menu_item'),
    path('delete/<str:item_id>/', delete_menu_item, name='delete_menu_item'),
    
    
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-register/', admin_register, name='admin_register'),
    path('admin/', include('core.admin_urls')),
]
