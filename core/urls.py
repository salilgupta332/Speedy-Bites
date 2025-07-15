from django.urls import path , include
from .views import (
    landing_page, 
    add_menu_item, 
    edit_menu_item, 
    delete_menu_item, 
    admin_register,
    user_register,
    user_login,
)
from . import views
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
def test(request):
    return HttpResponse("Core URLs working")

urlpatterns = [
    path('test/', test),
    path('', landing_page, name='landing'),

    # Menu routes (admin)
    path('add/', add_menu_item, name='add_menu_item'),
    path('edit/<str:item_id>/', edit_menu_item, name='edit_menu_item'),
    path('delete/<str:item_id>/', delete_menu_item, name='delete_menu_item'),

    # Auth
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-register/', admin_register, name='admin_register'),

    # Admin and User routes
    
    path('user/register/', user_register, name='user_register'),
    path('user/login/', user_login, name='user_login'),
]
