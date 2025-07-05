# core/urls.py

from django.urls import path
from . import views
from .views import home, add_menu_item, edit_menu_item, delete_menu_item,landing_page

urlpatterns = [
    path('', landing_page, name='landing'),
    path('', views.home, name='home'),
    path('add/', add_menu_item, name='add_menu_item'),
    path('edit/<str:item_id>/', edit_menu_item, name='edit_menu_item'),
    path('delete/<str:item_id>/', delete_menu_item, name='delete_menu_item'),
]
