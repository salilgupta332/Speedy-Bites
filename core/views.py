from django.shortcuts import render
from django.http import HttpResponse
from .models import MenuItem
from .forms import MenuItemForm
from django.shortcuts import render, redirect
import base64
from django.contrib import messages
from core.utils import admin_login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from .forms import AdminRegistrationForm
from .models import Admin_User
from .models import SiteUser
from .forms import UserRegisterForm, UserLoginForm
import random

@admin_login_required
def menu_dashboard(request):
    items = MenuItem.objects()
    return render(request, 'admin/menu_dashboard.html', {'menu_items': items})

@admin_login_required
def menu_dashboard(request):
    items = MenuItem.objects()
    return render(request, 'admin/menu_dashboard.html', {'menu_items': items})

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
            return redirect('menu_dashboard')
    else:
        form = MenuItemForm()
    return render(request, 'admin/add_item.html', {'form': form})


def delete_menu_item(request, item_id):
    item = MenuItem.objects.get(id=item_id)
    item.delete()
    return redirect('menu_dashboard')


def edit_menu_item(request, item_id):
    item = MenuItem.objects.get(id=item_id)

    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            item.name = form.cleaned_data['name']
            item.price = form.cleaned_data['price']
            item.description = form.cleaned_data['description']
            item.save()
            return redirect('menu_dashboard')
    else:
        # Pre-fill the form manually
        form = MenuItemForm(initial={
            'name': item.name,
            'price': item.price,
            'description': item.description,
        })

    return render(request, 'admin/edit_item.html', {'form': form})

def delete_menu_item(request, item_id):
    try:
        item = MenuItem.objects.get(id=item_id)
        item.delete()
        return redirect('menu_dashboard')
    except MenuItem.DoesNotExist:
        return HttpResponse("Item not found", status=404)

def landing_page(request):
    return render(request, 'landing.html')

def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

def admin_register(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            Admin_User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password'])  # 🔐 hashed
            ).save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('admin_login')  # or redirect to 'login'
    else:
        form = AdminRegistrationForm()

    return render(request, 'admin/admin_register.html', {'form': form})



from django.contrib.auth.hashers import check_password

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Admin_User.objects.get(username=username)
            if check_password(password, user.password):
                # ✅ Login success - store session
                request.session['admin_logged_in'] = True
                messages.success(request, "Login successful!")
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid password")
        except Admin_User.DoesNotExist:
            messages.error(request, "User not found")
    
    return render(request, 'admin/admin_login.html')

def admin_logout(request):
    print("Before logout:", request.session.items()) 
    request.session.flush()  # Clears all session data
    print("After logout:", request.session.items())
    return redirect('admin_login')  

# --- Step 3: User Auth Views START ---

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            SiteUser(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            ).save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('user_login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/user_register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = SiteUser.objects(username=form.cleaned_data['username'], password=form.cleaned_data['password']).first()
            if user:
                request.session['user_logged_in'] = True
                request.session['username'] = user.username
                return redirect('landing')  # or wherever
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = UserLoginForm()
    return render(request, 'user/user_login.html', {'form': form})
# --- Step 3: User Auth Views END ---

def reset_password(request, token):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user = SiteUser.objects(token=token).first()
        if user:
            user.password = new_password  # ⚠️ ideally hash it
            user.token = None  # clear token
            user.save()
            messages.success(request, 'Password reset successful. Please log in.')
            return redirect('user_login')
        else:
            messages.error(request, 'Invalid or expired token.')
            return redirect('forgot_password')

    return render(request, 'user/reset_password.html', {'token': token})

def send_otp_view(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        try:
            user = SiteUser.objects.get(mobile=mobile)
            otp = str(random.randint(100000, 999999))  # Generate 6-digit OTP
            user.otp = otp
            user.save()
            print(f"Generated OTP for {mobile}: {otp}")  # Simulate SMS sending
            request.session['mobile'] = mobile
            return redirect('verify_otp')  # move to step 3
        except SiteUser.DoesNotExist:
            messages.error(request, "Mobile number not registered.")
    return render(request, 'user/send_otp.html')


def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        mobile = request.session.get('mobile')

        if not mobile:
            messages.error(request, "Session expired. Please try again.")
            return redirect('send_otp')

        try:
            user = SiteUser.objects.get(mobile=mobile)
            if user.otp == entered_otp:
                messages.success(request, "OTP verified successfully!")
                return redirect('reset_password')  # Step 4
            else:
                messages.error(request, "Invalid OTP.")
        except SiteUser.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('send_otp')

    return render(request, 'user/verify_otp.html')

# core/views.py

def reset_password_view(request):
    mobile = request.session.get('mobile')
    
    if not mobile:
        messages.error(request, "Session expired. Please request a new OTP.")
        return redirect('send_otp')

    if request.method == 'POST':
        new_password = request.POST.get('password')

        try:
            user = SiteUser.objects.get(mobile=mobile)
            user.password = new_password
            user.save()
            messages.success(request, "Password reset successfully. Please log in.")
            return redirect('user_login')
        except SiteUser.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('send_otp')

    return render(request, 'user/reset_password.html')
