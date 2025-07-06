from django.shortcuts import render
from django.http import HttpResponse
from .models import MenuItem
from .forms import MenuItemForm
from django.shortcuts import render, redirect
import base64
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from .forms import AdminRegisterForm
from .models import Admin_User
from .forms import AdminRegistrationForm




def home(request):
    # Fetch all menu items
    items = MenuItem.objects()
    
    # Pass data to the template
    return render(request, 'home.html', {'menu_items': items})

def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES.get('image')
            image_data = None

            if image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')

            MenuItem(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],  # ✅ comma fixed here
                image_data=image_data
            ).save()
            return redirect('home')
    else:
        form = MenuItemForm()
    return render(request, 'core/add_item.html', {'form': form})


def delete_menu_item(request, item_id):
    item = MenuItem.objects.get(id=item_id)
    item.delete()
    return redirect('home')


def edit_menu_item(request, item_id):
    item = MenuItem.objects.get(id=item_id)

    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            item.name = form.cleaned_data['name']
            item.price = form.cleaned_data['price']
            item.description = form.cleaned_data['description']
            item.save()
            return redirect('home')
    else:
        # Pre-fill the form manually
        form = MenuItemForm(initial={
            'name': item.name,
            'price': item.price,
            'description': item.description,
        })

    return render(request, 'edit_item.html', {'form': form})

def delete_menu_item(request, item_id):
    try:
        item = MenuItem.objects.get(id=item_id)
        item.delete()
        return redirect('home')
    except MenuItem.DoesNotExist:
        return HttpResponse("Item not found", status=404)

def landing_page(request):
    return render(request, 'landing.html')

def admin_register(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            Admin_User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            ).save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('admin_register')  # or redirect to 'login'
    else:
        form = AdminRegistrationForm()

    return render(request, 'admin_register.html', {'form': form})

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')