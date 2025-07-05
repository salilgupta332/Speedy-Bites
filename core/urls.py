# core/urls.py

from django.urls import path
from .views import home, landing_page, add_menu_item, edit_menu_item, delete_menu_item

urlpatterns = [
    
    path('', landing_page, name='landing'),                     # Landing page
    path('menu/', home, name='home'),                           # Admin dashboard
    path('add/', add_menu_item, name='add_menu_item'),
    path('edit/<str:item_id>/', edit_menu_item, name='edit_menu_item'),
    path('delete/<str:item_id>/', delete_menu_item, name='delete_menu_item'),
]
