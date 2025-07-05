from django.shortcuts import render
from django.http import HttpResponse
from .models import MenuItem
from .forms import MenuItemForm
from django.shortcuts import render, redirect
import base64
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

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
    return render(request, 'add_item.html', {'form': form})


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

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "admin_login.html")

def admin_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Admin registered successfully. You can now log in.")
            return redirect('admin_login')

    return render(request, "admin_register.html")

def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in
            return redirect('home')  # Redirect to home or wherever
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})
