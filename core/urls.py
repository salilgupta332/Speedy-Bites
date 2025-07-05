# core/urls.py

from django.urls import path , include
from django.contrib import admin
from . import views
from .views import home, add_menu_item, edit_menu_item, delete_menu_item,landing_page

urlpatterns = [
    
    path('', include('core.urls')),
    path('', landing_page, name='landing'),              # This will load by default on "/"
    path('menu/', home, name='home'),                    # Admin panel
    path('add/', add_menu_item, name='add_menu_item'),
    path('edit/<str:item_id>/', edit_menu_item, name='edit_menu_item'),
    path('delete/<str:item_id>/', delete_menu_item, name='delete_menu_item'),
    path('admin/django/', admin.site.urls),
]
